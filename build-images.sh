#!/bin/bash

# Define image names and version
APP_IMAGE="aws-tf-gen-app:latest"
MYSQL_IMAGE="aws-tf-gen-mysql:latest"
REDIS_IMAGE="aws-tf-gen-redis:latest"

# Function to build an image
build_image() {
    local dockerfile=$1
    local image_name=$2
    echo "Building $image_name..."
    if [ ! -f "$dockerfile" ]; then
        echo "Error: Dockerfile not found at $dockerfile"
        exit 1
    fi
    docker build -f "$dockerfile" -t "$image_name" .
    if [ $? -eq 0 ]; then
        echo "Successfully built $image_name"
    else
        echo "Error: Failed to build $image_name"
        exit 1
    fi
}

# Check for required files
if [ ! -f "app/migrations/001_initial.sql" ]; then
    echo "Error: Migration file app/migrations/001_initial.sql not found"
    exit 1
fi

# Build each image
build_image "docker/app/Dockerfile" "$APP_IMAGE"
build_image "docker/mysql/Dockerfile" "$MYSQL_IMAGE"
build_image "docker/redis/Dockerfile" "$REDIS_IMAGE"

echo "All images built successfully!"