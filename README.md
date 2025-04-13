# AWS Terraform Generator

A production-grade web application to generate Terraform code for any AWS resource. Built with FastAPI, React.js, TypeScript, MySQL, Redis, and Docker.

## Features
- Dynamic configuration for any AWS resource using Terraform schemas.
- User authentication with JWT and refresh tokens.
- Rich UI with a resource wizard, real-time validation, and Terraform previews.
- Production-ready Docker setup with Nginx, Gunicorn, and optimized MySQL/Redis.
- Comprehensive tests and secure configurations.

## Prerequisites
- Docker and Docker Compose
- Node.js 20+ (for local frontend development)
- Python 3.10+ (for local backend development)

## Setup
1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd aws-terraform-generator