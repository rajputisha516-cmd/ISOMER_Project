#!/bin/bash

# Isomer - AI Surveillance System Startup Script
# This script starts both backend and frontend services

set -e

echo "🚀 Starting Isomer AI Surveillance System..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python
echo -e "${BLUE}Checking Python...${NC}"
if ! command -v python &> /dev/null; then
    echo -e "${RED}Python not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Check Node.js
echo -e "${BLUE}Checking Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js not found. Please install Node.js 16+${NC}"
    exit 1
fi

# Start Backend
echo -e "${BLUE}Starting Backend...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -q -r requirements.txt

# Start backend in background
python app.py &
BACKEND_PID=$!
echo -e "${GREEN}Backend started (PID: $BACKEND_PID)${NC}"

cd ..

# Wait for backend to be ready
echo -e "${BLUE}Waiting for backend to be ready...${NC}"
sleep 5

# Check if backend is running
if ! curl -s http://localhost:5000/api/health > /dev/null; then
    echo -e "${RED}Backend failed to start${NC}"
    exit 1
fi

echo -e "${GREEN}Backend is ready!${NC}"

# Start Frontend
echo -e "${BLUE}Starting Frontend...${NC}"
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install
fi

# Start frontend in background
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}Frontend started (PID: $FRONTEND_PID)${NC}"

echo ""
echo -e "${GREEN}✅ Isomer System Started Successfully!${NC}"
echo ""
echo "📊 Dashboard: http://localhost:3000"
echo "🔌 Backend API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Cleanup on exit
trap 'echo "Stopping services..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo "Services stopped"' EXIT

# Keep script running
wait
