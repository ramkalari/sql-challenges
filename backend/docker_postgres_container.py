import docker
import psycopg2
import tempfile
import uuid
import time
import os
from typing import Dict, Any, Optional
from challenges import CHALLENGES

class DockerPostgresContainer:
    """Manages isolated PostgreSQL containers for SQL challenges"""
    
    def __init__(self):
        self.docker_client = docker.from_env()
        self.active_containers = {}
        self.postgres_image = "postgres:15-alpine"
        self.default_password = "challenge_password"
        
    def create_challenge_container(self, challenge_id: int, user_id: str) -> Dict[str, Any]:
        """Create an isolated PostgreSQL container for a challenge"""
        
        # Get challenge details
        challenge = next((c for c in CHALLENGES if c["id"] == challenge_id), None)
        if not challenge:
            raise ValueError(f"Challenge {challenge_id} not found")
        
        # Create unique container name
        container_name = f"sql-challenge-{challenge_id}-{user_id}-{uuid.uuid4().hex[:8]}"
        
        try:
            # Create PostgreSQL container
            container = self.docker_client.containers.run(
                self.postgres_image,
                name=container_name,
                environment={
                    "POSTGRES_PASSWORD": self.default_password,
                    "POSTGRES_DB": "challenge_db",
                    "POSTGRES_USER": "challenge_user"
                },
                ports={'5432/tcp': None},  # Let Docker assign a random port
                detach=True,
                remove=True,  # Auto-remove when stopped
                mem_limit="256m",  # Limit memory usage
                cpu_period=100000,
                cpu_quota=50000,  # Limit CPU usage
                network_mode="bridge"
            )
            
            # Wait for container to be ready
            self._wait_for_postgres(container)
            
            # Get the assigned port
            container.reload()
            port = container.ports['5432/tcp'][0]['HostPort']
            
            # Create database connection string
            db_url = f"postgresql://challenge_user:{self.default_password}@localhost:{port}/challenge_db"
            
            # Initialize database with challenge schema and data
            self._setup_challenge_database(db_url, challenge)
            
            environment = {
                "container_name": container_name,
                "container_id": container.id,
                "db_url": db_url,
                "port": port,
                "challenge_id": challenge_id,
                "user_id": user_id
            }
            
            self.active_containers[container_name] = environment
            
            return environment
            
        except Exception as e:
            # Cleanup on error
            self._cleanup_container(container_name)
            raise Exception(f"Failed to create container: {str(e)}")
    
    def _wait_for_postgres(self, container, timeout=30):
        """Wait for PostgreSQL to be ready"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Check if container is running
                container.reload()
                if container.status != "running":
                    raise Exception("Container failed to start")
                
                # Try to connect to PostgreSQL
                logs = container.logs().decode()
                if "database system is ready to accept connections" in logs:
                    return
                
                time.sleep(1)
            except Exception:
                time.sleep(1)
        
        raise Exception("PostgreSQL container failed to start within timeout")
    
    def _setup_challenge_database(self, db_url: str, challenge: Dict[str, Any]):
        """Initialize database with challenge schema and seed data"""
        
        # Wait a bit for PostgreSQL to be fully ready
        time.sleep(2)
        
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        try:
            # Execute schema
            if challenge.get("schema"):
                cursor.execute(challenge["schema"])
            
            # Insert seed data
            if challenge.get("seed_data"):
                for statement in challenge["seed_data"]:
                    cursor.execute(statement)
            
            conn.commit()
        finally:
            conn.close()
    
    def execute_query(self, environment: Dict[str, Any], user_query: str) -> Dict[str, Any]:
        """Execute user query in isolated PostgreSQL container"""
        
        db_url = environment["db_url"]
        
        try:
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor()
            
            try:
                cursor.execute(user_query)
                
                if user_query.strip().upper().startswith("SELECT"):
                    results = cursor.fetchall()
                    columns = [description[0] for description in cursor.description] if cursor.description else []
                    
                    return {
                        "success": True,
                        "results": results,
                        "columns": columns,
                        "row_count": len(results)
                    }
                else:
                    conn.commit()
                    return {
                        "success": True,
                        "message": f"Query executed successfully. {cursor.rowcount} rows affected.",
                        "rows_affected": cursor.rowcount
                    }
                    
            except psycopg2.Error as e:
                return {
                    "success": False,
                    "error": str(e)
                }
            finally:
                conn.close()
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Database connection failed: {str(e)}"
            }
    
    def cleanup_container(self, environment: Dict[str, Any]):
        """Clean up PostgreSQL container"""
        try:
            container_name = environment["container_name"]
            
            if container_name in self.active_containers:
                del self.active_containers[container_name]
            
            self._cleanup_container(container_name)
            
        except Exception as e:
            print(f"Error cleaning up container: {e}")
    
    def _cleanup_container(self, container_name: str):
        """Stop and remove a container"""
        try:
            container = self.docker_client.containers.get(container_name)
            container.stop(timeout=5)
            container.remove()
        except docker.errors.NotFound:
            pass  # Container already removed
        except Exception as e:
            print(f"Error removing container {container_name}: {e}")
    
    def cleanup_all_containers(self):
        """Clean up all active containers"""
        for container_name in list(self.active_containers.keys()):
            self._cleanup_container(container_name)
        self.active_containers.clear()

class DockerChallengeManager:
    """Manages challenge execution with Docker PostgreSQL containers"""
    
    def __init__(self):
        self.container = DockerPostgresContainer()
    
    def execute_challenge(self, challenge_id: int, user_id: str, user_query: str) -> Dict[str, Any]:
        """Execute a challenge with user query in isolated PostgreSQL container"""
        
        # Create isolated container
        environment = self.container.create_challenge_container(challenge_id, user_id)
        
        try:
            # Execute user query
            result = self.container.execute_query(environment, user_query)
            
            # Validate against expected output
            if result["success"]:
                result["passed"] = self._validate_result(challenge_id, result)
            
            return result
            
        finally:
            # Clean up container
            self.container.cleanup_container(environment)
    
    def _validate_result(self, challenge_id: int, result: Dict[str, Any]) -> bool:
        """Validate user result against expected output"""
        challenge = next((c for c in CHALLENGES if c["id"] == challenge_id), None)
        if not challenge:
            return False
        
        expected_output = challenge.get("expected_output", [])
        
        # Simple validation - check if results match expected
        if "results" in result:
            user_results = result["results"]
            return user_results == expected_output
        
        return True

# Global challenge manager instance
docker_challenge_manager = DockerChallengeManager() 