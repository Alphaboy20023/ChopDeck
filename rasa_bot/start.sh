#!/bin/bash
# Make sure this file has Unix LF line endings

# Start actions server in background on port 5055
rasa run actions --port 5055 --enable-api &

# Start Rasa server using pre-trained model (no retraining, no TensorFlow needed)
rasa run \
  --enable-api \
  --cors "*" \
  --port $PORT \
  --interface 0.0.0.0 \
  --model models/20250922-135732-brass-music.tar.gz \
  --debug

# Keep container alive
wait
