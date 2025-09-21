FROM rasa/rasa:3.6.0
WORKDIR /app

# Copy requirements and install additional packages
COPY requirements.txt .
USER root
RUN pip install -r requirements.txt
COPY . .

# Train the model
RUN rasa train

USER 1001
EXPOSE 5005 5055
CMD ["rasa", "run", "--enable-api", "--cors", "*"]