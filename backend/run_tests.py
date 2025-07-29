#!/usr/bin/env python3
"""
Test runner for the SQL Challenges backend
"""

import subprocess
import sys
import os

def run_backend_tests():
    """Run backend tests using pytest"""
    print("🧪 Running Backend Tests...")
    print("=" * 50)
    
    try:
        # Install test dependencies if needed
        subprocess.run([
            sys.executable, "-m", "pip", "install", "pytest", "httpx"
        ], check=True, capture_output=True)
        
        # Run tests
        result = subprocess.run([
            sys.executable, "-m", "pytest", "test_main.py", "-v"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        return result.returncode == 0
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running tests: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def run_frontend_tests():
    """Run frontend tests using npm"""
    print("\n🧪 Running Frontend Tests...")
    print("=" * 50)
    
    try:
        # Change to frontend directory
        frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
        os.chdir(frontend_dir)
        
        # Install dependencies if needed
        subprocess.run(["npm", "install"], check=True, capture_output=True)
        
        # Run tests
        result = subprocess.run([
            "npm", "test", "--", "--watchAll=false", "--passWithNoTests"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        return result.returncode == 0
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running frontend tests: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main test runner"""
    print("🚀 SQL Challenges Test Suite")
    print("=" * 50)
    
    backend_success = run_backend_tests()
    frontend_success = run_frontend_tests()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"Backend Tests: {'✅ PASSED' if backend_success else '❌ FAILED'}")
    print(f"Frontend Tests: {'✅ PASSED' if frontend_success else '❌ FAILED'}")
    
    if backend_success and frontend_success:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n💥 Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 