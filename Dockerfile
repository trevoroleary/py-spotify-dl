# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Make port 80 available to the world outside this container
#EXPOSE 80

# Install the Python package
RUN pip install -e .

# Run app.py when the container launches
#CMD ["python", "./py_spotify_dl/run_server.py"]
CMD ["gunicorn", "-b", "0.0.0.0:8080", "download_track:app"]