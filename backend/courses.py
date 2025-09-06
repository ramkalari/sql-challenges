from challenges import CHALLENGES

COURSES = [
    {
        "id": "sql",
        "name": "SQL Fundamentals",
        "description": "Master SQL with hands-on challenges covering SELECT statements, JOINs, aggregations, and advanced queries. Practice with both SQLite and DuckDB engines.",
        "icon": "🗄️",
        "difficulty": "Beginner to Advanced",
        "duration": "4-6 weeks",
        "features": [
            "40+ SQL challenges",
            "SQLite & DuckDB support",
            "Real-world scenarios",
            "Progress tracking",
            "Leaderboard competition"
        ],
        "technologies": ["SQL", "SQLite", "DuckDB"],
        "challenge_ids": [c["id"] for c in CHALLENGES],  # All current challenges belong to SQL course
        "is_available": True
    },
    {
        "id": "python",
        "name": "Python Programming",
        "description": "Learn Python from basics to advanced concepts including data structures, algorithms, and real-world applications.",
        "icon": "🐍",
        "difficulty": "Beginner to Advanced",
        "duration": "6-8 weeks",
        "features": [
            "Coming soon",
            "Interactive coding challenges",
            "Project-based learning",
            "Automated testing"
        ],
        "technologies": ["Python", "Data Structures", "Algorithms"],
        "challenge_ids": [],  # Empty for now
        "is_available": False
    },
    {
        "id": "javascript",
        "name": "JavaScript Mastery",
        "description": "Modern JavaScript from fundamentals to advanced concepts including ES6+, async programming, and web development.",
        "icon": "⚡",
        "difficulty": "Beginner to Advanced", 
        "duration": "5-7 weeks",
        "features": [
            "Coming soon",
            "ES6+ features",
            "Async/await patterns",
            "DOM manipulation",
            "Testing with Jest"
        ],
        "technologies": ["JavaScript", "ES6+", "Node.js", "Testing"],
        "challenge_ids": [],  # Empty for now
        "is_available": False
    },
    {
        "id": "react",
        "name": "React Development",
        "description": "Build modern web applications with React, including hooks, state management, and component architecture.",
        "icon": "⚛️",
        "difficulty": "Intermediate to Advanced",
        "duration": "4-6 weeks", 
        "features": [
            "Coming soon",
            "React hooks",
            "State management",
            "Component patterns",
            "Testing strategies"
        ],
        "technologies": ["React", "TypeScript", "Next.js", "Testing Library"],
        "challenge_ids": [],  # Empty for now
        "is_available": False
    }
]

def get_course_by_id(course_id: str):
    """Get a course by its ID"""
    return next((course for course in COURSES if course["id"] == course_id), None)

def get_available_courses():
    """Get all available courses"""
    return [course for course in COURSES if course["is_available"]]

def get_course_challenges(course_id: str):
    """Get all challenges for a specific course"""
    course = get_course_by_id(course_id)
    if not course:
        return []
    
    # Filter challenges by the course's challenge_ids
    course_challenges = [c for c in CHALLENGES if c["id"] in course["challenge_ids"]]
    return course_challenges 