#!/bin/bash
set -e

echo "=== Starting Rasa Main Server on port $PORT ==="
exec rasa run \
  --cors "*" \
  --enable-api \
  --port $PORT \
  --interface 0.0.0.0 \
  --model models/20250922-135732-brass-music.tar.gz \
  --endpoints endpoints.yml \
  --credentials credentials.yml \
  --debug


# Service type: Web Service