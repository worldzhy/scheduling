# Build image
docker build -t scheduling:latest .

# Remove dangling images
docker image prune -f

# Remove container if still running
docker stop scheduling
docker rm scheduling

# Run image
docker run -d --name scheduling -p 3002:8080 scheduling:latest