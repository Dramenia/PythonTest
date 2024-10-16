# Base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy necessary files and install dependencies
COPY ../requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the container
COPY . /app/
ENV PYTHONUNBUFFERED=1

# Run the Python script
CMD ["python", "server.py"]
