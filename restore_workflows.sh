#!/bin/bash

# Configuration
BACKUP_DIR="./workflows"

echo "⬇️  Pulling latest changes from Git..."
git pull

echo "🔄 Importing workflows into n8n Docker container..."

# Find the running n8n container ID
CONTAINER_ID=$(docker ps -a -q --filter "ancestor=n8nio/n8n" | head -n 1)

if [ -z "$CONTAINER_ID" ]; then
  CONTAINER_ID=$(docker ps -a -q --filter "name=n8n" | head -n 1)
fi

if [ -z "$CONTAINER_ID" ]; then
  echo "❌ Error: No n8n container found."
  exit 1
fi

echo "🐳 Found n8n container: $CONTAINER_ID"

echo "🛑 Stopping n8n to release database lock..."
docker stop $CONTAINER_ID

echo "🔧 Fixing permissions on n8n_data..."
chown -R 1000:1000 n8n_data

echo "🔄 Importing workflows (using ephemeral container)..."
# Using the same image as the stopped container to ensure compatibility
IMAGE_NAME=$(docker inspect --format='{{.Config.Image}}' $CONTAINER_ID)

# Iterate and import
for file in $BACKUP_DIR/*.json; do
  echo "Importing $file..."
  # We use docker run with same volume mounts but override entrypoint to be safe
  docker run --rm \
  --user 1000:1000 \
  --entrypoint /bin/sh \
  -v $(pwd)/n8n_data:/home/node/.n8n \
  -v $(pwd)/$file:/tmp/workflow.json \
  $IMAGE_NAME \
  -c "n8n import:workflow --input=/tmp/workflow.json || echo '⚠️ Import failed for $file but continuing...'"
done

echo "✅ Import complete."

echo "🟢 Starting n8n..."
docker start $CONTAINER_ID

echo "✅ Import complete! Your VPS n8n is now up to date."
