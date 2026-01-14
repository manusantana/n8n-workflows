#!/bin/bash

# Configuration
BACKUP_DIR="./workflows"

echo "⬇️  Pulling latest changes from Git..."
git pull

echo "🔄 Importing workflows into n8n Docker container..."

# Import Workflows
# We use the same image as defined in docker-compose usually, or just n8nio/n8n
docker run --rm \
  -v $(pwd)/n8n_data:/home/node/.n8n \
  -v $(pwd)/$BACKUP_DIR:/backup \
  n8nio/n8n \
  n8n import:workflow --input=/backup/

echo "✅ Import complete! Your VPS n8n is now up to date."
