# Use a slim Python 3.10 image
FROM python:3.10.14-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system build deps needed for many ML packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential gcc git curl ca-certificates \
      libffi-dev libssl-dev libsndfile1 libatlas-base-dev libblas-dev liblapack-dev \
      && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Upgrade pip/build tools then install dependencies
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose default port and set command (adjust Gunicorn/project path if different)
EXPOSE 8000
CMD ["gunicorn", "ChopDeck.wsgi:application", "--bind", "0.0.0.0:8000"]
