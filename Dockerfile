# Used to build the image for the application
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app_1
COPY src .

RUN pip install Flask
RUN pip install requests
RUN pip install pyglet
RUN apt-get update && \
    apt-get install -y \
    python3-tk \
    tcl8.6 \
    tk8.6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

CMD ["python", "src"]
