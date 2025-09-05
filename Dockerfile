FROM python:3.10-slim
# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy only required application code (avoid secrets)
COPY snake.py .
# COPY app/ ./app   # if you have an app/ folder with modules

# Security best practice: use non-root user
RUN useradd -m appuser
USER appuser

# Run the application
CMD ["python", "snake.py"]
