import duckdb
import tempfile
import os
import uuid
from typing import Dict, Any, Optional
from challenges import CHALLENGES

class DuckDBContainer:
    """Manages isolated DuckDB database files for SQL challenges"""
    
    def __init__(self):
        self.active_environments = {}
        
    def create_challenge_environment(self, challenge_id: int, user_id: str) -> Dict[str, Any]:
        """Create an isolated environment for a challenge"""
        
        # Get challenge details
        challenge = next((c for c in CHALLENGES if c["id"] == challenge_id), None)
        if not challenge:
            raise ValueError(f"Challenge {challenge_id} not found")
        
        # Create unique container name
        container_name = f"duckdb-challenge-{challenge_id}-{user_id}-{uuid.uuid4().hex[:8]}"
        
        # Create temporary database file - DuckDB needs a proper path
        temp_dir = tempfile.mkdtemp()
        temp_db_path = os.path.join(temp_dir, f"challenge_{challenge_id}_{user_id}_{uuid.uuid4().hex[:8]}.duckdb")
        
        # Initialize database with challenge schema and data
        self._setup_challenge_database(temp_db_path, challenge)
        
        return {
            "container_name": container_name,
            "db_path": temp_db_path,
            "challenge_id": challenge_id,
            "user_id": user_id,
            "schema": challenge.get("schema", ""),
            "seed_data": challenge.get("seed_data", [])
        }
    
    def _setup_challenge_database(self, db_path: str, challenge: Dict[str, Any]):
        """Initialize database with challenge schema and seed data"""
        conn = duckdb.connect(db_path)
        
        try:
            # Execute schema - DuckDB can execute multiple statements separated by semicolons
            if challenge.get("schema_sql"):
                for statement in challenge["schema_sql"].split(';'):
                    statement = statement.strip()
                    if statement:  # Skip empty statements
                        conn.execute(statement)
            
            # Insert seed data
            if challenge.get("seed_sql"):
                for statement in challenge["seed_sql"].split(';'):
                    statement = statement.strip()
                    if statement:  # Skip empty statements
                        conn.execute(statement)
                
        finally:
            conn.close()
    
    def execute_query(self, environment: Dict[str, Any], user_query: str) -> Dict[str, Any]:
        """Execute user query in isolated environment"""
        
        db_path = environment["db_path"]
        conn = duckdb.connect(db_path)
        
        try:
            # Execute user query
            conn.execute(user_query)
            
            # Get results
            query_upper = user_query.strip().upper()
            if query_upper.startswith("SELECT") or query_upper.startswith("WITH"):
                results = conn.fetchall()
                columns = [desc[0] for desc in conn.description] if conn.description else []
                
                # Normalize results to strings to match expected format
                normalized_results = []
                for row in results:
                    normalized_row = [str(cell) for cell in row]
                    normalized_results.append(normalized_row)
                
                return {
                    "success": True,
                    "results": normalized_results,
                    "columns": columns,
                    "row_count": len(normalized_results)
                }
            else:
                # For non-SELECT queries (INSERT, UPDATE, DELETE, etc.)
                rowcount = conn.rowcount if hasattr(conn, 'rowcount') else 0
                return {
                    "success": True,
                    "message": f"Query executed successfully. {rowcount} rows affected.",
                    "rows_affected": rowcount
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            conn.close()
    
    def cleanup_environment(self, environment: Dict[str, Any]):
        """Clean up challenge environment"""
        try:
            # Remove temporary database file and directory
            db_path = environment["db_path"]
            if os.path.exists(db_path):
                os.unlink(db_path)
                # Also remove the temporary directory if empty
                temp_dir = os.path.dirname(db_path)
                if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                    os.rmdir(temp_dir)
        except Exception as e:
            print(f"Error cleaning up environment: {e}")

class DuckDBChallengeManager:
    """Manages DuckDB challenge execution and validation"""
    
    def __init__(self):
        self.container = DuckDBContainer()
    
    def execute_challenge(self, challenge_id: int, user_id: str, user_query: str) -> Dict[str, Any]:
        """Execute a challenge with user query"""
        
        # Create isolated environment
        environment = self.container.create_challenge_environment(challenge_id, user_id)
        
        try:
            # Execute user query
            result = self.container.execute_query(environment, user_query)
            
            # Validate against expected output
            if result["success"]:
                result["passed"] = self._validate_result(challenge_id, result)
            
            return result
            
        finally:
            # Clean up environment
            self.container.cleanup_environment(environment)
    
    def _validate_result(self, challenge_id: int, result: Dict[str, Any]) -> bool:
        """Validate user result against expected output"""
        challenge = next((c for c in CHALLENGES if c["id"] == challenge_id), None)
        if not challenge:
            return False
        
        expected_output = challenge.get("expected_output", [])
        
        # Simple validation - check if results match expected
        if "results" in result and result["results"] is not None:
            user_results = result["results"]
            return user_results == expected_output
        
        # If no results or results is None, it definitely doesn't match expected output
        return False

# Global DuckDB challenge manager instance
duckdb_challenge_manager = DuckDBChallengeManager() 