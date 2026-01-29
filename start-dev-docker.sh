#!/usr/bin/env bash

set -e

echo "Setting up the PingPong Study development environment..."

# Make sure the services are down to begin with
docker compose -p pingpong -f docker-compose.yml -f docker-compose.dev.yml down

# Update the PingPong study-srv image
docker compose -p pingpong -f docker-compose.yml -f docker-compose.dev.yml build study-srv

# Run the app
docker compose -p pingpong -f docker-compose.yml -f docker-compose.dev.yml up study-srv -d

# Wait until the pingpong server is ready
# The healthcheck command is `curl -f http://localhost:8001/health`
until docker exec pingpong-study-srv-1 curl -fs http://localhost:8001/health
do
  echo "Waiting for pingpong server to start..."
  sleep 1
done

echo ""
echo "All services are ready! 🏓"
