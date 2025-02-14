# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y poppler-utils

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
