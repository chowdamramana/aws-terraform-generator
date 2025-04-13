#!/bin/bash

COMPOSE_FILE="docker-compose.yml"

# Check for docker-compose.yml
if [ ! -f "$COMPOSE_FILE" ]; then
    echo "Error: Docker Compose file not found at $COMPOSE_FILE"
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Copy .env.example to .env and configure it."
    echo "Run: cp .env.example .env"
    exit 1
fi

# Default command
COMMAND="up -d"

# Handle command-line arguments
case "$1" in
    stop)
        COMMAND="down"
        ;;
    logs)
        COMMAND="logs -f"
        ;;
    build)
        echo "Running build-images.sh..."
        ./build-images.sh
        exit 0
        ;;
    *)
        if [ -n "$1" ]; then
            COMMAND="$@"
        fi
        ;;
esac

# Check for required images
for image in aws-tf-gen-app:latest aws-tf-gen-frontend:latest; do
    if ! docker image inspect "$image" > /dev/null 2>&1; then
        echo "Warning: Image $image not found. Running './build-images.sh' to build images."
        ./build-images.sh
        break
    fi
done

# Run Docker Compose
echo "Running Docker Compose with $COMPOSE_FILE..."
docker compose -f "$COMPOSE_FILE" $COMMAND

if [ $? -eq 0 ]; then
    echo "Docker Compose command executed successfully."
else
    echo "Error: Docker Compose command failed."
    exit 1
fi