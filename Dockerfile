# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files
COPY . .

# Expose the API port
EXPOSE 5000

# Run the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
