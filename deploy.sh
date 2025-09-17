#!/bin/bash

# Reddit Scraper Pro Deployment Script
# This script helps deploy the application in various environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    print_status "Installing requirements..."
    pip install -r requirements.txt
    
    print_success "Dependencies installed successfully!"
}

# Function to run the application
run_application() {
    print_status "Starting Reddit Scraper Pro..."
    source venv/bin/activate
    python src/main.py
}

# Function to run with Docker
run_docker() {
    print_status "Building Docker image..."
    docker build -t reddit-scraper-pro .
    
    print_status "Running Docker container..."
    docker run -p 5000:5000 reddit-scraper-pro
}

# Function to run with Docker Compose
run_docker_compose() {
    print_status "Starting with Docker Compose..."
    docker-compose up -d
    
    print_success "Application started! Visit http://localhost:5000"
}

# Function to run production deployment
run_production() {
    print_status "Setting up production deployment..."
    
    if [ ! -d "venv" ]; then
        install_dependencies
    fi
    
    source venv/bin/activate
    
    print_status "Installing Gunicorn..."
    pip install gunicorn
    
    print_status "Starting production server..."
    gunicorn --bind 0.0.0.0:5000 --workers 4 src.main:app
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    source venv/bin/activate
    
    if ! command_exists pytest; then
        print_status "Installing test dependencies..."
        pip install pytest pytest-cov flake8
    fi
    
    print_status "Running linting..."
    flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
    
    print_status "Running application startup test..."
    timeout 10s python src/main.py || code=$?
    if [[ $code -ne 124 && $code -ne 0 ]]; then
        print_error "Application failed to start"
        exit $code
    fi
    
    print_success "All tests passed!"
}

# Function to clean up
cleanup() {
    print_status "Cleaning up..."
    
    # Stop Docker containers
    if command_exists docker-compose; then
        docker-compose down 2>/dev/null || true
    fi
    
    # Remove virtual environment
    if [ -d "venv" ]; then
        rm -rf venv
        print_status "Removed virtual environment"
    fi
    
    # Remove Docker images
    if command_exists docker; then
        docker rmi reddit-scraper-pro 2>/dev/null || true
    fi
    
    print_success "Cleanup completed!"
}

# Function to show help
show_help() {
    echo "Reddit Scraper Pro Deployment Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  dev         Install dependencies and run in development mode"
    echo "  docker      Build and run with Docker"
    echo "  compose     Run with Docker Compose"
    echo "  production  Run in production mode with Gunicorn"
    echo "  test        Run tests and linting"
    echo "  clean       Clean up all generated files and containers"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 dev          # Development setup"
    echo "  $0 docker       # Docker deployment"
    echo "  $0 production   # Production deployment"
    echo ""
}

# Main script logic
main() {
    case "${1:-dev}" in
        "dev")
            print_status "Setting up development environment..."
            install_dependencies
            run_application
            ;;
        "docker")
            if ! command_exists docker; then
                print_error "Docker is not installed!"
                exit 1
            fi
            run_docker
            ;;
        "compose")
            if ! command_exists docker-compose; then
                print_error "Docker Compose is not installed!"
                exit 1
            fi
            run_docker_compose
            ;;
        "production")
            run_production
            ;;
        "test")
            install_dependencies
            run_tests
            ;;
        "clean")
            cleanup
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
}

# Check if Python is installed
if ! command_exists python3; then
    print_error "Python 3 is not installed!"
    exit 1
fi

# Run main function
main "$@"

