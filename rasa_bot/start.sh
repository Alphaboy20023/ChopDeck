#!/bin/bash

# Make sure this file uses Unix line endings (LF)
set -e  # Exit on any error

# Silence SQLAlchemy 2.0 warning
export SQLALCHEMY_SILENCE_UBER_WARNING=1

# Debug: Show environment
echo "PORT: $PORT"
echo "Current directory: $(pwd)"
echo "Files in directory: $(ls -la)"

# Train the model first (if needed)
echo "Training Rasa model..."
rasa train --force

# Start the actions server in the background
echo "Starting actions server..."
rasa run actions --port 5055 --enable-api --auto-reload &
ACTIONS_PID=$!

# Wait a moment for actions server to start
sleep 5

# Start the main Rasa server
echo "Starting main Rasa server on port $PORT..."
rasa run --enable-api \
  --cors "*" \
  --port $PORT \
  --host 0.0.0.0 \
  --endpoints endpoints.yml \
  --debug \
  --log-level DEBUG

# Clean up background process on exit
trap "kill $ACTIONS_PID 2>/dev/null || true" EXIT

# Keep container running
wait