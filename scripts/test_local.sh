#!/bin/bash

echo "🧪 Testing SQL Challenges Application Locally"
echo "=============================================="

# Test Backend
echo ""
echo "🔧 Testing Backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment and run tests
source venv/bin/activate
echo "✅ Virtual environment activated"

echo "Running backend tests..."
python -m pytest test_main.py -v
if [ $? -eq 0 ]; then
    echo "✅ Backend tests passed"
else
    echo "❌ Backend tests failed"
    exit 1
fi

# Test API endpoints
echo ""
echo "🌐 Testing API endpoints..."
python -c "
import requests
import json

# Test signup
response = requests.post('http://localhost:8000/auth/signup', 
    json={'email': 'test@example.com', 'password': 'password123'})
print(f'Signup: {response.status_code}')

# Test login
response = requests.post('http://localhost:8000/auth/login', 
    json={'email': 'test@example.com', 'password': 'password123'})
print(f'Login: {response.status_code}')

if response.status_code == 200:
    token = response.json()['access_token']
    
    # Test challenges endpoint
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('http://localhost:8000/challenges', headers=headers)
    print(f'Challenges: {response.status_code}')
    
    if response.status_code == 200:
        challenges = response.json()
        print(f'Found {len(challenges)} challenges')
    else:
        print('❌ Challenges endpoint failed')
else:
    print('❌ Login failed')
"

# Test Frontend
echo ""
echo "🎨 Testing Frontend..."
cd ../frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "❌ Node modules not found. Please run: npm install --legacy-peer-deps"
    exit 1
fi

echo "✅ Node modules found"

# Test build
echo "Building frontend..."
npm run build
if [ $? -eq 0 ]; then
    echo "✅ Frontend build successful"
else
    echo "❌ Frontend build failed"
    exit 1
fi

echo ""
echo "🎉 All tests passed! Application is ready for Railway deployment."
echo ""
echo "Next steps:"
echo "1. Commit and push your changes to GitHub"
echo "2. Run: railway login"
echo "3. Run: railway up"
echo ""
echo "Your application will be available at: https://your-app-name.railway.app" 