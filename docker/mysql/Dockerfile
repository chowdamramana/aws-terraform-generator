# Use official MySQL 8.0
FROM mysql:8.0

# Copy custom MySQL config
COPY docker/mysql/my.cnf /etc/mysql/conf.d/my.cnf

# Copy database initialization scripts
COPY app/migrations/001_initial.sql /docker-entrypoint-initdb.d/001_initial.sql

# Set environment variables for MySQL
ENV MYSQL_ROOT_PASSWORD=test123 \
    MYSQL_DATABASE=terraform_generator \
    MYSQL_USER=test \
    MYSQL_PASSWORD=test123

# Expose MySQL port
EXPOSE 3306