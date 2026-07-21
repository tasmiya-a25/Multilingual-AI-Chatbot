FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data required for English preprocessing
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('stopwords'); nltk.download('omw-1.4')"

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run with Gunicorn using Eventlet worker for Socket.IO support
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:5000", "api.app:app"]
