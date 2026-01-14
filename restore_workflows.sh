#!/bin/bash

# Configuration
BACKUP_DIR="./workflows"

echo "⬇️  Pulling latest changes from Git..."
git pull

echo "🔄 Importing workflows into n8n Docker container..."

# Find the running n8n container ID (more reliable than name)
CONTAINER_ID=$(docker ps -q --filter "ancestor=n8nio/n8n" | head -n 1)

if [ -z "$CONTAINER_ID" ]; then
  # Fallback: try finding by name if ancestor filter fails (user might use different image tag)
  CONTAINER_ID=$(docker ps -q --filter "name=n8n" | head -n 1)
fi

if [ -z "$CONTAINER_ID" ]; then
  echo "❌ Error: No running n8n container found. Please start n8n first."
  exit 1
fi

echo "🐳 Found n8n container: $CONTAINER_ID"

# Copy workflows to temp dir in container
echo "📂 Copying workflows to container..."
docker exec -u 0 $CONTAINER_ID mkdir -p /tmp/import_workflows
docker cp $BACKUP_DIR/. $CONTAINER_ID:/tmp/import_workflows/

# Fix permissions inside container to ensure 'node' user can read them
docker exec -u 0 $CONTAINER_ID chown -R node:node /tmp/import_workflows

# Run import command loop as 'node' user
echo "🔄 Executing n8n import for each file..."
docker exec -u node $CONTAINER_ID /bin/sh -c 'for file in /tmp/import_workflows/*.json; do echo "Importing $file..."; n8n import:workflow --input="$file"; done'

# Clean up
docker exec -u 0 $CONTAINER_ID rm -rf /tmp/import_workflows

echo "♻️  Restarting n8n to load new workflows..."
docker restart $CONTAINER_ID

echo "✅ Import complete! Your VPS n8n is now up to date."
