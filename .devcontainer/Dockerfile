# Use the official Python base image
FROM python:3.10.13

# Set the working directory
WORKDIR /workspace

# Copy the requirements.txt file and install dependencies
COPY requirements.txt /workspace/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /workspace

# Install Docker using the official Docker script
RUN apt-get update && apt-get install -y \
    curl && \
    curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh && \
    rm get-docker.sh

# Install Docker Compose
RUN curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Expose ports for the services
EXPOSE 8080 8501

# Set the default command to bash, so the container does not exit immediately
CMD ["bash"]
