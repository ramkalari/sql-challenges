# SQL Challenges - Interactive Learning Platform

A modern web application for learning SQL through interactive challenges. Students can sign up, practice SQL queries, and get instant feedback on their solutions.

## Features

- **User Authentication**: Sign up and login with email/password
- **Interactive SQL Challenges**: Practice with real database schemas
- **Instant Feedback**: Get immediate results and compare with expected output
- **Progress Tracking**: Track solved challenges and submission history
- **User Profiles**: View detailed progress statistics and submission history
- **Progressive Learning**: Challenges from basic to advanced levels
- **Modern UI**: Beautiful, responsive design with Tailwind CSS
- **JWT Authentication**: Secure token-based authentication

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLite**: Lightweight database for user management
- **JWT**: JSON Web Tokens for authentication
- **bcrypt**: Password hashing for security
- **Pydantic**: Data validation

### Frontend
- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Start the backend server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

1. **Landing Page**: Visit `http://localhost:3000` to see the landing page
2. **Sign Up**: Create a new account with your email and password
3. **Login**: Use your credentials to access the challenges
4. **Practice**: Select challenges and write SQL queries
5. **Get Feedback**: Submit queries and see instant results

## API Endpoints

### Authentication
- `POST /auth/signup` - Register a new user
- `POST /auth/login` - Login with credentials
- `GET /auth/me` - Get current user info (protected)

### Challenges
- `GET /challenges` - List all challenges with user progress
- `GET /challenges/{id}` - Get challenge details
- `POST /challenges/{id}/submit` - Submit a query for evaluation

### User Progress
- `GET /user/progress` - Get user's solved challenges
- `GET /user/submissions` - Get user's submission history

## Project Structure

```
sql_challenges/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── challenges.py        # Challenge definitions
│   ├── test_main.py         # Backend tests
│   ├── run_tests.py         # Test runner script
│   ├── requirements.txt     # Python dependencies
│   └── users.db            # SQLite database (created automatically)
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── page.tsx           # Home page (redirects)
│   │       ├── landing/
│   │       │   └── page.tsx       # Landing page with auth
│   │       ├── challenges/
│   │       │   └── page.tsx       # Protected challenges page
│   │       ├── profile/
│   │       │   └── page.tsx       # User profile page
│   │       ├── __tests__/         # Frontend tests
│   │       │   ├── landing.test.tsx
│   │       │   ├── challenges.test.tsx
│   │       │   └── profile.test.tsx
│   │       ├── layout.tsx         # Root layout
│   │       └── globals.css        # Global styles
│   ├── jest.config.js       # Jest configuration
│   ├── jest.setup.js        # Jest setup file
│   ├── package.json
│   └── README.md
└── README.md
```

## Security Features

- **Password Hashing**: Passwords are hashed using bcrypt
- **JWT Tokens**: Secure authentication with expiration
- **CORS Configuration**: Proper cross-origin resource sharing
- **Input Validation**: Pydantic models for data validation
- **SQL Injection Protection**: Parameterized queries

## Development

### Adding New Challenges

1. Edit `backend/challenges.py`
2. Add new challenge objects to the `CHALLENGES` list
3. Include schema SQL, seed data, and expected output

### Customizing the UI

1. Modify components in `frontend/src/app/`
2. Update styles using Tailwind CSS classes
3. Add new pages by creating directories in the app folder

## Testing

### Backend Tests

The backend uses pytest for testing. Tests cover:
- Authentication (signup, login, token validation)
- Challenge endpoints (listing, details, submission)
- User progress tracking
- Database functions

To run backend tests:
```bash
cd backend
python run_tests.py
```

Or run tests directly:
```bash
cd backend
python -m pytest test_main.py -v
```

### Frontend Tests

The frontend uses Jest and React Testing Library. Tests cover:
- Component rendering
- User interactions
- Authentication flows
- API integration
- Responsive design

To run frontend tests:
```bash
cd frontend
npm test
```

Or run with coverage:
```bash
cd frontend
npm run test:coverage
```

### Running All Tests

To run both backend and frontend tests:
```bash
cd backend
python run_tests.py
```

## Troubleshooting

### Common Issues

1. **Backend won't start**: Check if port 8000 is available
2. **Frontend won't start**: Check if port 3000 is available
3. **Authentication errors**: Ensure backend is running on localhost:8000
4. **Database errors**: Delete `users.db` to reset the database
5. **Test failures**: Install test dependencies with `pip install pytest httpx` for backend and `npm install` for frontend

### Logs

- Backend logs are displayed in the terminal running uvicorn
- Frontend logs are available in the browser console
- Test results are displayed in the terminal

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License. 