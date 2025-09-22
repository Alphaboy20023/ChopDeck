#!/bin/bash
set -e

echo "=== Starting Rasa Action Server on port 5055 ==="
exec rasa run actions --port 5055 --debug

# Background Worker