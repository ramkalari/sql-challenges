#!/bin/bash

# SQL Challenges Environment Setup Script

set -e

echo "🚀 Setting up environment variables for SQL Challenges..."

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

# Check if .env file exists
if [ -f ".env" ]; then
    print_warning ".env file already exists. Backing up to .env.backup"
    cp .env .env.backup
fi

# Create .env file
print_status "Creating .env file..."

cat > .env << 'EOF'
# Backend Environment Variables
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_URL=sqlite:///users.db
ENVIRONMENT=development

# Email Configuration
# Development (Mailtrap)
MAILTRAP_HOST=smtp.mailtrap.io
MAILTRAP_PORT=2525
MAILTRAP_USERNAME=your-mailtrap-username
MAILTRAP_PASSWORD=your-mailtrap-password

# Production (Resend SMTP)
# RESEND_SMTP_HOST=smtp.resend.com
# RESEND_SMTP_PORT=587
# RESEND_SMTP_USERNAME=resend
# RESEND_API_KEY=your-resend-api-key

# Email Settings
FROM_EMAIL=noreply@sqlchallenges.com
FRONTEND_URL=http://localhost:3000

# Frontend Environment Variables
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF

print_status ".env file created successfully!"

print_warning "Next steps:"
echo "1. Get Mailtrap credentials from https://mailtrap.io"
echo "2. Update MAILTRAP_USERNAME and MAILTRAP_PASSWORD in .env"
echo "3. For production, get Resend API key from https://resend.com"
echo "4. Update RESEND_API_KEY in .env for production"
echo "5. Generate a secure SECRET_KEY (you can use: openssl rand -hex 32)"
echo "6. Update the SECRET_KEY in .env"

print_status "Environment setup complete! 🎉" 