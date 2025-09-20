# Base image
FROM python:3.11-slim

# Set environment
ENV PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# Copy everything
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install rasa[full] asgiref  # Ensure Rasa and async helpers are installed

# Expose ports for Django and Rasa
EXPOSE 8000 5005 5055

# Start Django + Rasa
CMD bash -c "\
python manage.py migrate && \
python manage.py collectstatic --noinput && \
rasa run --enable-api --cors '*' --port 5005 & \
rasa run actions --port 5055 & \
gunicorn ChopDeck.wsgi:application --bind 0.0.0.0:8000"
