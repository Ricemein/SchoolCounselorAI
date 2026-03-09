#!/bin/bash
# Frontend setup and run script

# Load nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Navigate to frontend directory
cd "$(dirname "$0")"

echo "Installing dependencies..."
npm install

echo ""
echo "Starting development server..."
npm run dev
