# Base image
FROM python:3.11-slim

# Setting environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Setting work directory
WORKDIR /app

# Installing system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Installing Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copying project files
COPY . .

# Make start.sh executable
RUN chmod +x /app/start.sh

# Exposing the port
EXPOSE 8000

# Run the app with start.sh - migration, create superuser, collectstatic and gunicorn
CMD ["/app/start.sh"]