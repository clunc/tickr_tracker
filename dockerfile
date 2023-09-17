# Use the official Python image from the Docker Hub
FROM python:3.11

RUN apt-get update && apt-get upgrade -y && apt-get install bluez -y

# Add the Python script to the image
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt

# Run the application
CMD ["python", "main.py"]
