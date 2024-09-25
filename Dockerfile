# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy all dependency files
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 5000

# Run the application on 0.0.0.0
CMD ["python", "app.py", "--host=0.0.0.0"]
