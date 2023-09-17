# Use the official Python image from the Docker Hub
FROM python:3.11

RUN apt-get update && apt-get upgrade -y && apt-get install bluez -y

# Install dependencies
RUN pip install bleak asyncpg

# Add the Python script to the image
ADD . /app
WORKDIR /app

# Run the application
CMD ["python", "main.py"]
