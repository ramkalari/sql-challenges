#!/bin/bash

# SQL Challenges Railway Deployment Script

set -e

echo "🚀 Deploying SQL Challenges to Railway..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Railway CLI is installed
check_railway_cli() {
    if ! command -v railway &> /dev/null; then
        print_error "Railway CLI is not installed. Please install it first:"
        echo "npm install -g @railway/cli"
        exit 1
    fi
}

# Login to Railway
login_to_railway() {
    print_status "Logging in to Railway..."
    railway login
}

# Deploy to Railway
deploy_to_railway() {
    print_status "Deploying to Railway..."
    railway up
}

# Set environment variables
set_environment_variables() {
    print_status "Setting environment variables..."
    
    # Generate a secure secret key
    SECRET_KEY=$(openssl rand -hex 32)
    
    railway variables set SECRET_KEY="$SECRET_KEY"
    railway variables set DATABASE_PATH="users.db"
    
    print_status "Environment variables set successfully!"
}

# Show deployment info
show_deployment_info() {
    print_status "Getting deployment information..."
    
    # Get the deployed URL
    DEPLOY_URL=$(railway status --json | jq -r '.url')
    
    echo ""
    echo "🎉 Deployment successful!"
    echo ""
    echo "Your application is available at:"
    echo "  Backend API: $DEPLOY_URL"
    echo "  API Documentation: $DEPLOY_URL/docs"
    echo ""
    echo "Next steps:"
    echo "  1. Deploy frontend to Vercel"
    echo "  2. Update frontend environment variables"
    echo "  3. Test the application"
    echo ""
}

# Main deployment function
main() {
    print_status "Starting Railway deployment..."
    
    check_railway_cli
    login_to_railway
    set_environment_variables
    deploy_to_railway
    show_deployment_info
    
    print_status "Deployment complete! 🎉"
}

# Run main function
main "$@" 