#!/bin/bash

# SQL Challenges Setup Script
# This script sets up the development environment for the SQL Challenges project

set -e

echo "🚀 Setting up SQL Challenges development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8+"
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+"
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm"
        exit 1
    fi
    
    print_status "All requirements satisfied!"
}

# Setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Install test dependencies
    print_status "Installing test dependencies..."
    pip install pytest pytest-cov httpx
    
    cd ..
    print_status "Backend setup complete!"
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    print_status "Frontend setup complete!"
    cd ..
}

# Create environment file
create_env_file() {
    print_status "Creating environment file..."
    
    if [ ! -f ".env" ]; then
        cp env.example .env
        print_status "Created .env file from template"
    else
        print_warning ".env file already exists, skipping..."
    fi
}

# Run tests
run_tests() {
    print_status "Running tests..."
    
    # Backend tests
    print_status "Running backend tests..."
    cd backend
    source venv/bin/activate
    python -m pytest test_main.py -v
    cd ..
    
    # Frontend tests
    print_status "Running frontend tests..."
    cd frontend
    npm test -- --watchAll=false
    cd ..
    
    print_status "All tests completed!"
}

# Main setup function
main() {
    print_status "Starting SQL Challenges setup..."
    
    check_requirements
    setup_backend
    setup_frontend
    create_env_file
    
    print_status "Setup complete! 🎉"
    echo ""
    echo "To start the development servers:"
    echo ""
    echo "Backend:"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  uvicorn main:app --reload --host 0.0.0.0 --port 8000"
    echo ""
    echo "Frontend:"
    echo "  cd frontend"
    echo "  npm run dev"
    echo ""
    echo "The application will be available at:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8000"
    echo "  API Documentation: http://localhost:8000/docs"
    echo ""
    
    # Ask if user wants to run tests
    read -p "Would you like to run tests now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_tests
    fi
}

# Run main function
main "$@" 