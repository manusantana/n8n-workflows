#!/bin/bash

# Configuration
BACKUP_DIR="./workflows"
DATE=$(date +"%Y-%m-%d %H:%M:%S")

# Ensure backup directory exists
mkdir -p $BACKUP_DIR

echo "🔄 Exporting workflows and credentials from n8n Docker container..."

# Export Workflows (using running container to avoid DB locks)
# We assume the container name is usually project_folder-n8n-1.
# Here we try to detect it or use the likely name.
CONTAINER_NAME=$(docker ps --format "{{.Names}}" | grep n8n | head -n 1)

if [ -z "$CONTAINER_NAME" ]; then
  echo "❌ Error: n8n container not found is it running?"
  exit 1
fi

echo "🔌 Connecting to container $CONTAINER_NAME..."

# Execute export command inside the container
# 1. Create temp directory
docker exec $CONTAINER_NAME mkdir -p /tmp/workflows/

# 2. Export separately (--backup implies --separate --pretty --all)
docker exec $CONTAINER_NAME n8n export:workflow --backup --output=/tmp/workflows/

# 3. Copy to host
docker cp $CONTAINER_NAME:/tmp/workflows/. $BACKUP_DIR/

# 4. Cleanup container temp
docker exec $CONTAINER_NAME rm -rf /tmp/workflows/


# Export Credentials (optional - be careful committing these to public repos!)
# Remove the comment below if you want to backup credentials (encrypted)
# docker run --rm \
#   -v $(pwd)/n8n_data:/home/node/.n8n \
#   -v $(pwd)/$BACKUP_DIR:/backup \
#   n8nio/n8n \
#   n8n export:credentials --all --output=/backup/credentials.json

echo "✅ Export complete."

# Git Operations
echo "📦 Adding changes to Git..."
git add .

echo "📝 Committing..."
git commit -m "n8n Backup: $DATE"

echo "🚀 Pushing to repository..."
git push origin master

echo "🎉 Done! Workflows are safely stored in Git."
