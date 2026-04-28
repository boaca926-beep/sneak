#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check for --rebuild flag
REBUILD=""
if [ "$1" = "--rebuild" ]; then
    REBUILD="--build"
    echo -e "${YELLOW}Rebuilding image...${NC}"
fi

echo -e "${GREEN}🐍 Starting Snake Game...${NC}"

# Allow Docker to access X11 display
xhost +local:docker

# Set display environment variable
export DISPLAY=$DISPLAY

# Run the game
docker-compose up $REBUILD

# Cleanup after game closes
echo -e "${YELLOW}Cleaning up...${NC}"
xhost -local:docker
docker-compose down

echo -e "${GREEN}Game closed!${NC}"
