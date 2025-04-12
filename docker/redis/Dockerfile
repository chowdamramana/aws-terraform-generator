# Use official Redis 7.0
FROM redis:7.0-alpine

# Copy custom Redis config
COPY docker/redis/redis.conf /usr/local/etc/redis/redis.conf

# Expose Redis port
EXPOSE 6379

# Run Redis with custom config
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]