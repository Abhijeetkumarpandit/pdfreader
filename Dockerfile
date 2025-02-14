# Use official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the port (Render uses dynamic ports)
ENV PORT=10000
EXPOSE $PORT

# Start the app
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
