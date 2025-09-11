FROM python:3.10-slim
RUN apt-get update && apt-get install -y \
    python3-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy game + Flask wrapper
COPY app/sgame.py .
COPY app/app.py .

EXPOSE 5000

# Security best practice: use non-root user
RUN useradd -m appuser
USER appuser

# Run the Flask API
CMD ["python", "app.py"]
