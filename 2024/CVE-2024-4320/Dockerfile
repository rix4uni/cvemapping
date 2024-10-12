# Base image
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Copy project files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Expose port
EXPOSE 9600

# Run the application
CMD ["uvicorn", "poc:app", "--host", "0.0.0.0", "--port", "9600"]
