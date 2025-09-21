FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install only necessary system dependencies (removed ML packages)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential gcc curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Upgrade pip/build tools then install dependencies
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Collect static files for production
RUN python manage.py collectstatic --noinput --clear

# Expose port
EXPOSE 8000

# Use gunicorn for production
CMD ["gunicorn", "ChopDeck.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]