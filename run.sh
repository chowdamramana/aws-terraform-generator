#!/bin/bash

# Define the Docker Compose file
COMPOSE_FILE="docker-compose.yml"

# Check if the Docker Compose file exists
if [ ! -f "$COMPOSE_FILE" ]; then
    echo "Error: Docker Compose file not found at $COMPOSE_FILE"
    exit 1
fi

# Default command
COMMAND="up -d"

# Parse arguments
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

# Check if images exist, suggest building if not
for image in aws-tf-gen-app:latest aws-tf-gen-mysql:latest aws-tf-gen-redis:latest; do
    if ! docker image inspect "$image" > /dev/null 2>&1; then
        echo "Warning: Image $image not found. Please run './build-images.sh' first."
        exit 1
    fi
done

# Run Docker Compose
echo "Running Docker Compose with $COMPOSE_FILE..."
docker-compose -f "$COMPOSE_FILE" $COMMAND

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo "Docker Compose command executed successfully."
else
    echo "Error: Docker Compose command failed."
    exit 1
fi