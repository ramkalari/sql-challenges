import pytest
from fastapi.testclient import TestClient
from main import app
import sqlite3
import os

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Setup and teardown test database"""
    # Remove test database if it exists
    if os.path.exists("test_users.db"):
        os.remove("test_users.db")
    
    # Create test database
    conn = sqlite3.connect("test_users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            challenge_id INTEGER NOT NULL,
            solved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            attempts INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, challenge_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            challenge_id INTEGER NOT NULL,
            query TEXT NOT NULL,
            passed BOOLEAN NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    conn.commit()
    conn.close()
    
    yield
    
    # Cleanup
    if os.path.exists("test_users.db"):
        os.remove("test_users.db")

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_signup_success(self):
        """Test successful user signup"""
        response = client.post("/auth/signup", json={
            "email": "test@example.com",
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["email"] == "test@example.com"
        assert data["token_type"] == "bearer"
    
    def test_signup_duplicate_email(self):
        """Test signup with existing email"""
        # First signup
        client.post("/auth/signup", json={
            "email": "duplicate@example.com",
            "password": "password123"
        })
        
        # Second signup with same email
        response = client.post("/auth/signup", json={
            "email": "duplicate@example.com",
            "password": "password456"
        })
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_signup_invalid_email(self):
        """Test signup with invalid email"""
        response = client.post("/auth/signup", json={
            "email": "invalid-email",
            "password": "password123"
        })
        assert response.status_code == 422
    
    def test_login_success(self):
        """Test successful login"""
        # First signup
        client.post("/auth/signup", json={
            "email": "login@example.com",
            "password": "password123"
        })
        
        # Then login
        response = client.post("/auth/login", json={
            "email": "login@example.com",
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["email"] == "login@example.com"
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = client.post("/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]
    
    def test_get_current_user(self):
        """Test getting current user info"""
        # Signup and get token
        signup_response = client.post("/auth/signup", json={
            "email": "current@example.com",
            "password": "password123"
        })
        token = signup_response.json()["access_token"]
        
        # Get current user
        response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json()["email"] == "current@example.com"
    
    def test_get_current_user_invalid_token(self):
        """Test getting current user with invalid token"""
        response = client.get("/auth/me", headers={"Authorization": "Bearer invalid-token"})
        assert response.status_code == 401

class TestChallenges:
    """Test challenge endpoints"""
    
    def test_get_challenges_unauthorized(self):
        """Test getting challenges without authentication"""
        response = client.get("/challenges")
        assert response.status_code == 401
    
    def test_get_challenges_authorized(self):
        """Test getting challenges with authentication"""
        # Signup and get token
        signup_response = client.post("/auth/signup", json={
            "email": "challenges@example.com",
            "password": "password123"
        })
        token = signup_response.json()["access_token"]
        
        # Get challenges
        response = client.get("/challenges", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        challenges = response.json()
        assert isinstance(challenges, list)
        assert len(challenges) > 0
        
        # Check challenge structure
        challenge = challenges[0]
        assert "id" in challenge
        assert "name" in challenge
        assert "level" in challenge
        assert "solved" in challenge
        assert "attempts" in challenge
    
    def test_get_challenge_details(self):
        """Test getting specific challenge details"""
        response = client.get("/challenges/1")
        assert response.status_code == 200
        challenge = response.json()
        assert "id" in challenge
        assert "name" in challenge
        assert "question" in challenge
        assert "schema_tables" in challenge
        assert "level" in challenge
    
    def test_get_nonexistent_challenge(self):
        """Test getting a challenge that doesn't exist"""
        response = client.get("/challenges/999")
        assert response.status_code == 404
        assert "Challenge not found" in response.json()["detail"]

class TestChallengeSubmission:
    """Test challenge submission functionality"""
    
    def test_submit_query_unauthorized(self):
        """Test submitting query without authentication"""
        response = client.post("/challenges/1/submit", json={
            "user_query": "SELECT * FROM products"
        })
        assert response.status_code == 401
    
    def test_submit_correct_query(self):
        """Test submitting a correct query"""
        # Signup and get token
        signup_response = client.post("/auth/signup", json={
            "email": "submit@example.com",
            "password": "password123"
        })
        token = signup_response.json()["access_token"]
        
        # Submit correct query
        response = client.post("/challenges/1/submit", 
            json={"user_query": "SELECT * FROM products"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["passed"] == True
        assert "result" in data
        assert "column_names" in data
    
    def test_submit_incorrect_query(self):
        """Test submitting an incorrect query"""
        # Signup and get token
        signup_response = client.post("/auth/signup", json={
            "email": "incorrect@example.com",
            "password": "password123"
        })
        token = signup_response.json()["access_token"]
        
        # Submit incorrect query
        response = client.post("/challenges/1/submit", 
            json={"user_query": "SELECT name FROM products"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["passed"] == False
        assert "result" in data
        assert "expected" in data
    
    def test_submit_invalid_sql(self):
        """Test submitting invalid SQL"""
        # Signup and get token
        signup_response = client.post("/auth/signup", json={
            "email": "invalid@example.com",
            "password": "password123"
        })
        token = signup_response.json()["access_token"]
        
        # Submit invalid SQL
        response = client.post("/challenges/1/submit", 
            json={"user_query": "SELECT * FROM nonexistent_table"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 400
        assert "no such table" in response.json()["detail"].lower()

class TestUserProgress:
    """Test user progress tracking"""
    
    def test_get_user_progress(self):
        """Test getting user progress"""
        # Signup and get token
        signup_response = client.post("/auth/signup", json={
            "email": "progress@example.com",
            "password": "password123"
        })
        token = signup_response.json()["access_token"]
        
        # Get user progress
        response = client.get("/user/progress", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        data = response.json()
        assert "progress" in data
        assert isinstance(data["progress"], list)
    
    def test_get_user_submissions(self):
        """Test getting user submissions"""
        # Signup and get token
        signup_response = client.post("/auth/signup", json={
            "email": "submissions@example.com",
            "password": "password123"
        })
        token = signup_response.json()["access_token"]
        
        # Get user submissions
        response = client.get("/user/submissions", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        data = response.json()
        assert "submissions" in data
        assert isinstance(data["submissions"], list)
    
    def test_progress_tracking(self):
        """Test that progress is tracked when solving challenges"""
        # Signup and get token
        signup_response = client.post("/auth/signup", json={
            "email": "tracking@example.com",
            "password": "password123"
        })
        token = signup_response.json()["access_token"]
        
        # Submit a correct query
        client.post("/challenges/1/submit", 
            json={"user_query": "SELECT * FROM products"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Check that progress is recorded
        progress_response = client.get("/user/progress", headers={"Authorization": f"Bearer {token}"})
        progress_data = progress_response.json()
        
        # Should have at least one solved challenge
        assert len(progress_data["progress"]) >= 1
        
        # Check that the challenge is marked as solved
        solved_challenge = progress_data["progress"][0]
        assert solved_challenge["challenge_id"] == 1
        assert solved_challenge["attempts"] >= 1

class TestDatabaseFunctions:
    """Test database helper functions"""
    
    def test_parse_table_schema(self):
        """Test parsing table schema"""
        from main import parse_table_schema
        
        schema_sql = """
        CREATE TABLE products (
          id INTEGER PRIMARY KEY,
          name TEXT,
          price INTEGER,
          category TEXT
        );
        """
        
        tables = parse_table_schema(schema_sql)
        assert len(tables) == 1
        table = tables[0]
        assert table["table_name"] == "products"
        assert len(table["columns"]) == 4
        
        # Check column details
        columns = table["columns"]
        assert columns[0]["name"] == "id"
        assert columns[0]["type"] == "INTEGER"
        assert "PRIMARY KEY" in columns[0]["constraints"]
        
        assert columns[1]["name"] == "name"
        assert columns[1]["type"] == "TEXT"

if __name__ == "__main__":
    pytest.main([__file__]) 