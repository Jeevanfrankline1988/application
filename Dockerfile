# Use slim Python image
FROM python:3.10-slim

# Install dependencies for Pygame
RUN apt-get update && apt-get install -y \
    python3-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy game code + Flask wrapper
COPY app/sgame.py .
COPY app/app.py .

# Copy HTML templates
COPY app/templates/ /app/templates/

# Expose Flask port
EXPOSE 5000

# Create non-root user and give ownership of /app
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Run Flask
CMD ["python", "app.py"]
