#!/bin/bash
# Make sure this file uses Unix line endings (LF)

# Silence SQLAlchemy 2.0 warning
export SQLALCHEMY_SILENCE_UBER_WARNING=1

# Start the actions server in the background on its own internal port
rasa run actions --port 5055 --enable-api &

# Start the main Rasa server on Render's assigned port
rasa run --enable-api --cors "*" --port $PORT --debug

# Keep container running
wait
