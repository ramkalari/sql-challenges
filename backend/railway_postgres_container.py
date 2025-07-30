import os
import psycopg2
import tempfile
import uuid
from typing import Dict, Any, Optional
from challenges import CHALLENGES
import asyncio
import aiohttp

class RailwayPostgresContainer:
    """Manages isolated PostgreSQL databases for SQL challenges using Railway"""
    
    def __init__(self):
        self.railway_token = os.getenv("RAILWAY_TOKEN")
        self.railway_project_id = os.getenv("RAILWAY_PROJECT_ID")
        self.base_db_url = os.getenv("DATABASE_URL")
        
    async def create_challenge_database(self, challenge_id: int, user_id: str) -> Dict[str, Any]:
        """Create an isolated PostgreSQL database for a challenge"""
        
        # Get challenge details
        challenge = next((c for c in CHALLENGES if c["id"] == challenge_id), None)
        if not challenge:
            raise ValueError(f"Challenge {challenge_id} not found")
        
        # Create unique database name
        db_name = f"challenge_{challenge_id}_{user_id}_{uuid.uuid4().hex[:8]}"
        
        # Create database via Railway API
        db_url = await self._create_railway_database(db_name)
        
        # Initialize database with challenge schema and data
        await self._setup_challenge_database(db_url, challenge)
        
        return {
            "db_name": db_name,
            "db_url": db_url,
            "challenge_id": challenge_id,
            "user_id": user_id
        }
    
    async def _create_railway_database(self, db_name: str) -> str:
        """Create a new PostgreSQL database via Railway API"""
        
        if not self.railway_token or not self.railway_project_id:
            # Fallback to local PostgreSQL or SQLite for development
            return self._create_local_database(db_name)
        
        # Railway API endpoint
        url = f"https://backboard.railway.app/graphql/v2"
        
        # GraphQL mutation to create database
        mutation = """
        mutation CreateDatabase($input: CreateDatabaseInput!) {
            createDatabase(input: $input) {
                id
                name
                connectionString
            }
        }
        """
        
        variables = {
            "input": {
                "name": db_name,
                "projectId": self.railway_project_id,
                "type": "POSTGRESQL"
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.railway_token}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={
                "query": mutation,
                "variables": variables
            }, headers=headers) as response:
                data = await response.json()
                
                if "errors" in data:
                    raise Exception(f"Failed to create database: {data['errors']}")
                
                return data["data"]["createDatabase"]["connectionString"]
    
    def _create_local_database(self, db_name: str) -> str:
        """Create a local database for development"""
        # For development, use SQLite with unique file
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db_path = temp_db.name
        temp_db.close()
        
        return f"sqlite:///{temp_db_path}"
    
    async def _setup_challenge_database(self, db_url: str, challenge: Dict[str, Any]):
        """Initialize database with challenge schema and seed data"""
        
        if db_url.startswith("sqlite"):
            # SQLite setup
            import sqlite3
            db_path = db_url.replace("sqlite:///", "")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            try:
                # Execute schema
                if challenge.get("schema"):
                    cursor.executescript(challenge["schema"])
                
                # Insert seed data
                if challenge.get("seed_data"):
                    for statement in challenge["seed_data"]:
                        cursor.execute(statement)
                
                conn.commit()
            finally:
                conn.close()
        else:
            # PostgreSQL setup
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
    
    async def execute_query(self, environment: Dict[str, Any], user_query: str) -> Dict[str, Any]:
        """Execute user query in isolated PostgreSQL environment"""
        
        db_url = environment["db_url"]
        
        if db_url.startswith("sqlite"):
            # SQLite execution
            import sqlite3
            db_path = db_url.replace("sqlite:///", "")
            conn = sqlite3.connect(db_path)
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
                    
            except sqlite3.Error as e:
                return {
                    "success": False,
                    "error": str(e)
                }
            finally:
                conn.close()
        else:
            # PostgreSQL execution
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
    
    async def cleanup_database(self, environment: Dict[str, Any]):
        """Clean up challenge database"""
        try:
            db_url = environment["db_url"]
            
            if db_url.startswith("sqlite"):
                # Remove SQLite file
                db_path = db_url.replace("sqlite:///", "")
                if os.path.exists(db_path):
                    os.unlink(db_path)
            else:
                # Drop PostgreSQL database via Railway API
                await self._drop_railway_database(environment["db_name"])
                
        except Exception as e:
            print(f"Error cleaning up database: {e}")
    
    async def _drop_railway_database(self, db_name: str):
        """Drop a PostgreSQL database via Railway API"""
        
        if not self.railway_token:
            return
        
        url = f"https://backboard.railway.app/graphql/v2"
        
        mutation = """
        mutation DeleteDatabase($input: DeleteDatabaseInput!) {
            deleteDatabase(input: $input) {
                id
            }
        }
        """
        
        variables = {
            "input": {
                "name": db_name,
                "projectId": self.railway_project_id
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.railway_token}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            await session.post(url, json={
                "query": mutation,
                "variables": variables
            }, headers=headers)

class RailwayChallengeManager:
    """Manages challenge execution with Railway PostgreSQL"""
    
    def __init__(self):
        self.container = RailwayPostgresContainer()
    
    async def execute_challenge(self, challenge_id: int, user_id: str, user_query: str) -> Dict[str, Any]:
        """Execute a challenge with user query in isolated PostgreSQL"""
        
        # Create isolated database
        environment = await self.container.create_challenge_database(challenge_id, user_id)
        
        try:
            # Execute user query
            result = await self.container.execute_query(environment, user_query)
            
            # Validate against expected output
            if result["success"]:
                result["passed"] = self._validate_result(challenge_id, result)
            
            return result
            
        finally:
            # Clean up database
            await self.container.cleanup_database(environment)
    
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
railway_challenge_manager = RailwayChallengeManager() 