#!/bin/bash
# Start actions server in background
rasa run actions --port 5055 &

# Start Rasa server in foreground
exec rasa run --enable-api --cors "*" --port $PORT --debug
