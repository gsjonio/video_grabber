# vidgrab — YouTube downloader in Docker
# Usage: docker build -t vidgrab .
#        docker run -v /downloads:/data vidgrab https://youtu.be/dQw4w9WgXcQ

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml poetry.lock* ./
COPY vidgrab/ ./vidgrab/

# Install dependencies
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

# Create data volume
RUN mkdir -p /data
WORKDIR /data

# Default command
ENTRYPOINT ["vidgrab"]
CMD ["--help"]
