#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if .env file exists
echo -e "${YELLOW}Checking if .env file exists...${NC}"

if [ ! -f .env_example ]; then
    echo -e "\n${RED}.env_example does not exist!${NC}"
else
    if [ ! -f .env ]; then
        cp .env_example .env
        echo -e "\n${GREEN}Copied .env_example to .env${NC}"
    else
        echo -e "\n${GREEN}.env file already exists${NC}"
    fi
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    Snake Game Launcher${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Function to fix Docker permissions
fix_docker_permissions() {
    echo -e "${YELLOW}Fixing Docker permissions...${NC}"
    
    # Add user to docker group
    sudo usermod -aG docker $USER 2>/dev/null
    
    # Fix socket permissions for current session
    sudo chmod 666 /var/run/docker.sock 2>/dev/null
    
    echo -e "${GREEN}✅ Docker permissions fixed${NC}"
    echo -e "${YELLOW}Note: You may need to run 'newgrp docker' for permanent fix${NC}"
    echo ""
}

# Check Docker
echo -e "${YELLOW}Checking Docker installation...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo -e "${YELLOW}Installing Docker...${NC}"
    
    sudo apt update
    sudo apt install -y docker.io docker-compose-plugin
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $USER
    
    echo -e "${GREEN}✅ Docker installed${NC}"
    echo -e "${YELLOW}⚠️ Please run: newgrp docker${NC}"
    echo -e "${YELLOW}Then run: ./run.sh${NC}"
    exit 0
fi

echo -e "${GREEN}✅ Docker found: $(docker --version)${NC}"

# Check if Docker is accessible - try to start if not
if ! docker version &> /dev/null; then
    echo -e "${YELLOW}Starting Docker daemon...${NC}"
    sudo systemctl start docker
    sleep 3
    
    if docker version &> /dev/null; then
        echo -e "${GREEN}✅ Docker is now running${NC}"
    else
        echo -e "${RED}❌ Cannot connect to Docker${NC}"
        echo -e "${YELLOW}Attempting to fix permissions...${NC}"
        fix_docker_permissions
        
        if docker version &> /dev/null; then
            echo -e "${GREEN}✅ Fixed! Docker is now accessible${NC}"
        else
            echo -e "${RED}❌ Still cannot connect to Docker${NC}"
            echo -e "${YELLOW}Please try: newgrp docker${NC}"
            echo -e "${YELLOW}Then run: ./run.sh${NC}"
            exit 1
        fi
    fi
else
    echo -e "${GREEN}✅ Docker daemon is running${NC}"
fi

# Check permissions
if ! docker ps &> /dev/null; then
    echo -e "${YELLOW}⚠️ Permission issue detected${NC}"
    fix_docker_permissions
    
    if docker ps &> /dev/null; then
        echo -e "${GREEN}✅ Permission fixed!${NC}"
    else
        echo -e "${RED}❌ Still have permission issues${NC}"
        echo -e "${YELLOW}Please run: newgrp docker${NC}"
        echo -e "${YELLOW}Then run: ./run.sh${NC}"
        exit 0
    fi
fi

echo -e "${GREEN}✅ Docker is ready!${NC}"

# Check for --rebuild flag
PORT=5000
REBUILD=""
if [ "$1" = "--rebuild" ]; then
    REBUILD="--build"
    echo -e "${YELLOW}Rebuilding image...${NC}"
fi

echo -e "\n${GREEN}🐍 Starting Snake Game...${NC}"

# Free port 5000
echo "Checking for processes using port $PORT..."
PIDS=$(lsof -ti :$PORT 2>/dev/null)
if [ -n "$PIDS" ]; then
    echo "Killing process(es): $PIDS"
    kill -9 $PIDS 2>/dev/null
    echo "Processes killed."
else
    echo "No process found using port $PORT."
fi

sleep 1

# Deduplicate scores
echo "Cleaning duplicate scores..."
if [ -f scores.db ] && command -v python3 &> /dev/null; then
    python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('scores.db')
    conn.execute('''
        DELETE FROM scores
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM scores
            GROUP BY player_name, score, substr(timestamp, 1, 19)
        )
    ''')
    conn.commit()
    deleted = conn.total_changes
    conn.close()
    if deleted > 0:
        print(f'Removed {deleted} duplicate rows.')
    else:
        print('No duplicates found')
except Exception as e:
    pass
" 2>/dev/null
else
    echo "No scores.db yet – skipping deduplication."
fi

# Setup display
if command -v xhost &> /dev/null; then
    xhost +local:docker 2>/dev/null
fi
export DISPLAY=$DISPLAY

# Start game
echo -e "\n${GREEN}Starting Docker containers...${NC}"
docker compose up $REBUILD

# Cleanup
echo -e "\n${YELLOW}Cleaning up...${NC}"
if command -v xhost &> /dev/null; then
    xhost -local:docker 2>/dev/null
fi
docker compose down 2>/dev/null

echo -e "${GREEN}✨ Game closed!${NC}"
