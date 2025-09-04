# Use slim Python base image
FROM python:3.11-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install required system dependencies (alphabetically sorted )
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-dev \
    libsm6 \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libxext6 \
    libxrender-dev \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Security best practice: use non-root user
RUN useradd -m appuser
USER appuser

# Run the application
CMD ["python", "snake.py"]
