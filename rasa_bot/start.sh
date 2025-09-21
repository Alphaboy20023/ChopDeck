    #!/bin/bash
    rasa run actions --port 5055 &
    rasa run --enable-api --cors "*" --port $PORT --debug

    # Keep container running
    wait