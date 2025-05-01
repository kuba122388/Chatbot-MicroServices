FROM python:3.9-slim

# Dependency installation
RUN pip install pika google-generativeai pymongo python-dotenv

# Setting work directory
WORKDIR /app

# App files copy to container
COPY . .

# Run the application
CMD [ "python", "worker.py" ]
