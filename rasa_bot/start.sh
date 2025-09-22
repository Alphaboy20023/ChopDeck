#!/bin/bash
# Make sure this file has Unix LF line endings

# Start actions server in background
rasa run actions --port $PORT --enable-api &

# Start Rasa server using pre-trained model (no retraining, no TensorFlow needed)
rasa run --enable-api --cors "*" --port $PORT --model models/20250921-121233.tar.gz --debug

# Keep container alive
wait
