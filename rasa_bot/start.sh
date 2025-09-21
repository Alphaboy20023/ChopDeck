#!/bin/bash
# Start actions server in background
rasa run actions --port 5055 &

# Start API server on main port
rasa run --enable-api --cors "*" --port $PORT --debug

# Keep container running
wait