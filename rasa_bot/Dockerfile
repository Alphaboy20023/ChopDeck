FROM rasa/rasa:3.6.0

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
USER root
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install "sqlalchemy<2.0"  # Fix SQLAlchemy warning

# Copy the rest of the project
COPY . .

# Train the model
RUN rasa train

# Set non-root user for runtime
USER 1001

# Expose the port Render assigns
EXPOSE $PORT

# Start script
CMD ["bash", "./start.sh"]
