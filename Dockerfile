# Base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy necessary files and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the root files and necessary folders
COPY . /app/
ENV PYTHONUNBUFFERED=1
# Run the Python client script
CMD ["python", "client.py"]
