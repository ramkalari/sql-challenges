from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
import sqlite3
import re
import jwt
import bcrypt
import os
from datetime import datetime, timedelta, timezone
from challenges import CHALLENGES
from challenge_container import challenge_manager

app = FastAPI()
security = HTTPBearer()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CORS Configuration
# Environment-aware CORS setup
ENVIRONMENT = os.getenv("ENVIRONMENT", "production").lower()
ALLOW_ALL_ORIGINS = os.getenv("ALLOW_ALL_ORIGINS", "false").lower() == "true"

if ALLOW_ALL_ORIGINS:
    origins = ["*"]
elif ENVIRONMENT == "development":
    origins = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]
else:
    # Production - only allow specific deployed domains
    origins = [
        "https://sql-challenges-two.vercel.app",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
def get_database_path():
    return os.getenv("DATABASE_PATH", "users.db")

# Database initialization
def init_db():
    conn = sqlite3.connect(get_database_path())
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create user_progress table to track solved challenges
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
    
    # Create user_submissions table to store all submissions
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

init_db()

# Models
class UserSignup(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ChallengeSubmitRequest(BaseModel):
    user_query: str

# Authentication functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def get_user_id(email: str) -> int:
    """Get user ID from email"""
    conn = sqlite3.connect(get_database_path())
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        conn.close()

def record_submission(user_id: int, challenge_id: int, query: str, passed: bool):
    """Record a user submission"""
    conn = sqlite3.connect(get_database_path())
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO user_submissions (user_id, challenge_id, query, passed)
            VALUES (?, ?, ?, ?)
        """, (user_id, challenge_id, query, passed))
        conn.commit()
    finally:
        conn.close()

def update_user_progress(user_id: int, challenge_id: int, passed: bool):
    """Update user progress for a challenge"""
    conn = sqlite3.connect(get_database_path())
    cursor = conn.cursor()
    try:
        # Start transaction
        conn.execute("BEGIN TRANSACTION")
        
        if passed:
            # Check if already solved
            cursor.execute("""
                SELECT id FROM user_progress 
                WHERE user_id = ? AND challenge_id = ?
            """, (user_id, challenge_id))
            
            if not cursor.fetchone():
                # First time solving
                cursor.execute("""
                    INSERT INTO user_progress (user_id, challenge_id, attempts)
                    VALUES (?, ?, 1)
                """, (user_id, challenge_id))
            else:
                # Already solved, just update attempts
                cursor.execute("""
                    UPDATE user_progress 
                    SET attempts = attempts + 1
                    WHERE user_id = ? AND challenge_id = ?
                """, (user_id, challenge_id))
        else:
            # Failed attempt, increment attempts if already solved
            cursor.execute("""
                UPDATE user_progress 
                SET attempts = attempts + 1
                WHERE user_id = ? AND challenge_id = ?
            """, (user_id, challenge_id))
            
            # If not solved yet, create entry with 1 attempt
            if cursor.rowcount == 0:
                cursor.execute("""
                    INSERT INTO user_progress (user_id, challenge_id, attempts)
                    VALUES (?, ?, 1)
                """, (user_id, challenge_id))
        
        # Commit transaction
        conn.commit()
    except Exception as e:
        # Rollback transaction on error
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_user_progress(user_id: int):
    """Get user's progress across all challenges"""
    if user_id is None:
        return []
        
    conn = sqlite3.connect(get_database_path())
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT challenge_id, solved_at, attempts
            FROM user_progress 
            WHERE user_id = ?
            ORDER BY solved_at DESC
        """, (user_id,))
        return cursor.fetchall()
    finally:
        conn.close()

def get_user_submissions(user_id: int, challenge_id: int = None):
    """Get user's submissions, optionally filtered by challenge"""
    conn = sqlite3.connect(get_database_path())
    cursor = conn.cursor()
    try:
        if challenge_id:
            cursor.execute("""
                SELECT challenge_id, query, passed, submitted_at
                FROM user_submissions 
                WHERE user_id = ? AND challenge_id = ?
                ORDER BY submitted_at DESC
            """, (user_id, challenge_id))
        else:
            cursor.execute("""
                SELECT challenge_id, query, passed, submitted_at
                FROM user_submissions 
                WHERE user_id = ?
                ORDER BY submitted_at DESC
            """, (user_id,))
        return cursor.fetchall()
    finally:
        conn.close()

def parse_table_schema(schema_sql: str):
    """Parse CREATE TABLE SQL and return structured schema data"""
    tables = []
    
    # Split by CREATE TABLE statements
    create_table_regex = re.compile(r'CREATE TABLE (\w+)\s*\(([\s\S]*?)\);', re.IGNORECASE)
    matches = create_table_regex.findall(schema_sql)
    
    for table_name, columns_text in matches:
        columns = []
        
        # Parse columns
        column_lines = [line.strip() for line in columns_text.split(',') if line.strip()]
        
        for line in column_lines:
            # Skip foreign key constraints
            if line.upper().startswith('FOREIGN KEY') or line.upper().startswith('PRIMARY KEY'):
                continue
            
            # Parse column definition
            column_match = re.match(r'^(\w+)\s+([\w()]+)(.*)$', line)
            if column_match:
                column_name = column_match.group(1)
                column_type = column_match.group(2)
                constraints_text = column_match.group(3)
                
                # Extract constraints
                constraints = []
                if 'PRIMARY KEY' in constraints_text.upper():
                    constraints.append('PRIMARY KEY')
                if 'NOT NULL' in constraints_text.upper():
                    constraints.append('NOT NULL')
                if 'UNIQUE' in constraints_text.upper():
                    constraints.append('UNIQUE')
                
                columns.append({
                    "name": column_name,
                    "type": column_type,
                    "constraints": constraints
                })
        
        tables.append({
            "table_name": table_name,
            "columns": columns
        })
    
    return tables

@app.post("/auth/signup")
def signup(user: UserSignup):
    conn = sqlite3.connect(get_database_path())
    cursor = conn.cursor()
    
    try:
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password and create user
        password_hash = hash_password(user.password)
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (user.email, password_hash)
        )
        conn.commit()
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "email": user.email
        }
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        conn.close()

@app.post("/auth/login")
def login(user: UserLogin):
    conn = sqlite3.connect(get_database_path())
    cursor = conn.cursor()
    
    try:
        # Get user by email
        cursor.execute("SELECT password_hash FROM users WHERE email = ?", (user.email,))
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        password_hash = result[0]
        
        # Verify password
        if not verify_password(user.password, password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "email": user.email
        }
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        conn.close()

@app.get("/auth/me")
def get_current_user(email: str = Depends(verify_token)):
    return {"email": email}

@app.get("/user/progress")
def get_user_progress_endpoint(email: str = Depends(verify_token)):
    user_id = get_user_id(email)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    progress = get_user_progress(user_id)
    
    # Convert to more readable format
    progress_data = []
    for challenge_id, solved_at, attempts in progress:
        challenge = next((c for c in CHALLENGES if c["id"] == challenge_id), None)
        if challenge:
            progress_data.append({
                "challenge_id": challenge_id,
                "challenge_name": challenge["name"],
                "level": challenge["level"],
                "solved_at": solved_at,
                "attempts": attempts
            })
    
    return {"progress": progress_data}

@app.get("/user/submissions")
def get_user_submissions_endpoint(email: str = Depends(verify_token), challenge_id: int = None):
    user_id = get_user_id(email)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    submissions = get_user_submissions(user_id, challenge_id)
    
    # Convert to more readable format
    submissions_data = []
    for c_id, query, passed, submitted_at in submissions:
        challenge = next((c for c in CHALLENGES if c["id"] == c_id), None)
        submissions_data.append({
            "challenge_id": c_id,
            "challenge_name": challenge["name"] if challenge else f"Challenge {c_id}",
            "query": query,
            "passed": passed,
            "submitted_at": submitted_at
        })
    
    return {"submissions": submissions_data}

@app.get("/challenges")
def get_challenges(email: str = Depends(verify_token)):
    user_id = get_user_id(email)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user progress
    progress = get_user_progress(user_id)
    progress_dict = {p[0]: {"solved_at": p[1], "attempts": p[2]} for p in progress}
    
    # Return challenges with progress info
    challenges_with_progress = []
    for c in CHALLENGES:
        challenge_data = {
            "id": c["id"], 
            "name": c["name"], 
            "level": c["level"]
        }
        
        if c["id"] in progress_dict:
            challenge_data["solved"] = True
            challenge_data["solved_at"] = progress_dict[c["id"]]["solved_at"]
            challenge_data["attempts"] = progress_dict[c["id"]]["attempts"]
        else:
            challenge_data["solved"] = False
            challenge_data["attempts"] = 0
        
        challenges_with_progress.append(challenge_data)
    
    return challenges_with_progress

def get_next_challenge(user_id: int) -> dict | None:
    """Get the next unsolved challenge with least complexity for a user"""
    if user_id is None:
        return None
        
    level_order = {"Basic": 1, "Intermediate": 2, "Advanced": 3}
    
    # Get user's solved challenges
    progress = get_user_progress(user_id)
    solved_ids = {p[0] for p in progress}
    
    # Get unsolved challenges sorted by complexity
    unsolved_challenges = [
        c for c in CHALLENGES 
        if c["id"] not in solved_ids
    ]
    
    if not unsolved_challenges:
        return None
    
    # Sort by level complexity, then by ID
    unsolved_challenges.sort(key=lambda c: (level_order[c["level"]], c["id"]))
    
    next_challenge = unsolved_challenges[0]
    return {
        "id": next_challenge["id"],
        "name": next_challenge["name"],
        "level": next_challenge["level"]
    }

@app.get("/challenges/next")
def get_next_challenge_endpoint(email: str = Depends(verify_token)):
    """Get the next challenge for the user"""
    user_id = get_user_id(email)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    next_challenge = get_next_challenge(user_id)
    if not next_challenge:
        return {"message": "All challenges completed!", "next_challenge": None}
    
    return {"next_challenge": next_challenge}

@app.get("/challenges/{challenge_id}")
def get_challenge(challenge_id: int):
    challenge = next((c for c in CHALLENGES if c["id"] == challenge_id), None)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    # Parse the schema SQL into structured data
    schema_tables = parse_table_schema(challenge["schema_sql"])
    
    return {
        "id": challenge["id"], 
        "name": challenge["name"], 
        "question": challenge["question"], 
        "schema_tables": schema_tables,
        "level": challenge["level"]
    }

@app.get("/challenges/next")
def get_next_challenge_endpoint(email: str = Depends(verify_token)):
    """Get the next challenge for the user"""
    user_id = get_user_id(email)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    next_challenge = get_next_challenge(user_id)
    if not next_challenge:
        return {"message": "All challenges completed!", "next_challenge": None}
    
    return {"next_challenge": next_challenge}

@app.post("/challenges/{challenge_id}/submit")
def submit_query(challenge_id: int, req: ChallengeSubmitRequest, email: str = Depends(verify_token)):
    challenge = next((c for c in CHALLENGES if c["id"] == challenge_id), None)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    try:
        # Get user ID for isolated execution
        user_id = get_user_id(email)
        if not user_id:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Execute query in isolated container environment
        result = challenge_manager.execute_challenge(challenge_id, str(user_id), req.user_query)
        
        # Record submission and progress
        if user_id:
            record_submission(user_id, challenge_id, req.user_query, result.get("passed", False))
            update_user_progress(user_id, challenge_id, result.get("passed", False))
        
        if result["success"]:
            if result.get("passed", False):
                # Get next challenge info when current challenge is passed
                next_challenge = get_next_challenge(user_id)
                return {
                    "passed": True, 
                    "result": result.get("results", []), 
                    "column_names": result.get("columns", []),
                    "next_challenge": next_challenge
                }
            else:
                return {
                    "passed": False, 
                    "result": result.get("results", []), 
                    "expected": challenge["expected_output"], 
                    "column_names": result.get("columns", []),
                    "expected_column_names": challenge.get("expected_column_names", [])
                }
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Query execution failed"))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
