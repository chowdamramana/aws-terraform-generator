#!/bin/bash

# Image names for the project
APP_IMAGE="aws-tf-gen-app:latest"
FRONTEND_IMAGE="aws-tf-gen-frontend:latest"

# Function to build a Docker image
build_image() {
    local dockerfile=$1
    local image_name=$2
    local context=$3
    echo "Building $image_name..."
    if [ ! -f "$dockerfile" ]; then
        echo "Error: Dockerfile not found at $dockerfile"
        exit 1
    fi
    docker build -f "$dockerfile" -t "$image_name" "$context"
    if [ $? -eq 0 ]; then
        echo "Successfully built $image_name"
    else
        echo "Error: Failed to build $image_name"
        exit 1
    fi
}

# Build images
build_image "docker/app/Dockerfile" "$APP_IMAGE" .
build_image "docker/frontend/Dockerfile" "$FRONTEND_IMAGE" .

echo "All images built successfully!"