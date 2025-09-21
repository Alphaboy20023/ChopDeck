#!/bin/bash
# Make sure this is Unix line endings (LF)

# Start actions server in background
rasa run actions --port 5055 &

# Start Rasa server with API enabled
rasa run --enable-api --cors "*" --port $PORT --debug

# Keep container running
wait
