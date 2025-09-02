#!/bin/bash

# Start DuckDB-enabled SQL Challenges for testing

echo "🦆 Starting SQL Challenges with DuckDB support..."

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

echo "📦 Starting backend..."
cd backend

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Start backend in background
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo "🚀 Backend started on http://localhost:8000 (PID: $BACKEND_PID)"

# Go back to project root
cd ..

echo "📦 Starting frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📥 Installing frontend dependencies..."
    npm install
fi

# Start frontend in background
npm run dev &
FRONTEND_PID=$!
echo "🚀 Frontend started on http://localhost:3000 (PID: $FRONTEND_PID)"

# Go back to project root
cd ..

echo ""
echo "🎉 Both services are running!"
echo "📊 Backend API: http://localhost:8000"
echo "🌐 Frontend: http://localhost:3000"
echo "📖 API Documentation: http://localhost:8000/docs"
echo ""
echo "🦆 DuckDB support is now available in the challenges page!"
echo "Users can switch between SQLite and DuckDB engines."
echo ""
echo "Press Ctrl+C to stop both services..."

# Function to cleanup processes
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set trap to cleanup on Ctrl+C
trap cleanup SIGINT

# Wait for user to stop
wait 