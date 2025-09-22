# pip install --no-cache-dir --upgrade rasa==3.6.21 rasa-sdk==3.6.2

# #!/bin/bash
# # Make sure this file has Unix LF line endings

# # Start actions server in background on port 5055
# rasa run actions --port 5055 --debug &

# # Start Rasa server using pre-trained model (no retraining, no TensorFlow needed)
# rasa run \
#   --cors "*" \
#   --port $PORT \
#   --interface 0.0.0.0 \
#   --model models/20250922-135732-brass-music.tar.gz \
#   --credentials credentials.yml \
#   --debug

# # Keep container alive
# wait


#!/bin/bash
set -e  # Exit on any error

echo "=== Starting Actions Server ==="
rasa run actions --port 5055 --debug &
ACTIONS_PID=$!

echo "=== Waiting 5 seconds for actions server ==="
sleep 5

echo "=== Starting Main Rasa Server on port $PORT ==="
echo "PORT is: $PORT"
echo "Model file exists: $(ls -la models/)"

# Add explicit error handling
rasa run \
  --cors "*" \
  --port $PORT \
  --interface 0.0.0.0 \
  --model models/20250922-135732-brass-music.tar.gz \
  --credentials credentials.yml \
  --debug 2>&1 | tee rasa_server.log &

RASA_PID=$!

# Wait for both processes
wait $RASA_PID