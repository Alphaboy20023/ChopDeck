pip install --no-cache-dir --upgrade rasa==3.6.21 rasa-sdk==3.6.2

#!/bin/bash
# Make sure this file has Unix LF line endings

# Start actions server in background on port 5055
rasa run actions --port 5055 --debug &

# Start Rasa server using pre-trained model (no retraining, no TensorFlow needed)
rasa run \
  --cors "*" \
  --port $PORT \
  --interface 0.0.0.0 \
  --model models/20250922-135732-brass-music.tar.gz \
  --credentials credentials.yml \
  --debug

# Keep container alive
wait
