FROM rasa/rasa:3.6.0
WORKDIR /app

COPY requirements.txt .
USER root
RUN pip install -r requirements.txt
RUN pip install "sqlalchemy<2.0"  # Fix SQLAlchemy warning
COPY . .

RUN rasa train

USER 1001
EXPOSE $PORT

# Use environment variable PORT that Render provides
CMD rasa run --enable-api --cors "*" --port $PORT --debug