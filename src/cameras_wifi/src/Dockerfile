# Example of a multi-architecture base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install necessary libraries
RUN apt-get update && apt-get install -y libopencv-dev python3-opencv
RUN pip install face_recognition PyJWT flask

# Copy the local code to the container
COPY . /app

# Expose the port the app runs on
EXPOSE 4298

# Command to run the app
CMD ["python", "app.py"]
