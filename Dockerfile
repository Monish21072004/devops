# Use an official Python runtime as the base image.
FROM python:3.9-slim

# Install system dependencies including Xvfb to simulate a display if needed.
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libportaudio2 \
    portaudio19-dev \
    ffmpeg \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory.
WORKDIR /app

# Copy requirements.txt and install Python dependencies.
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your application code.
COPY . /app

# Set environment variables for Flask and to disable desktop-dependent modules.
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=1
ENV DISABLE_KEYBOARD_LISTENER=true
ENV DISABLE_MOUSE_TRACKER=true

# Run the Flask application using xvfb-run.

CMD ["flask", "run", "--host=0.0.0.0"]
