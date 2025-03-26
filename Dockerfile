# Use an official Python runtime as the base image.
FROM python:3.9-slim

# Install system dependencies.
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libportaudio2 \
    portaudio19-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory.
WORKDIR /app

# Create a temporary directory for pip builds.
RUN mkdir -p /app/tmp
ENV TMPDIR=/app/tmp

# Copy requirements.txt and install Python dependencies.
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your application code.
COPY . /app

# Set environment variables for Flask and disable desktop-dependent modules.
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=1
ENV TF_CPP_MIN_LOG_LEVEL=2
ENV DISABLE_KEYBOARD_LISTENER=true
ENV DISABLE_MOUSE_TRACKER=true

# Start the Flask application.
CMD ["flask", "run", "--host=0.0.0.0"]
