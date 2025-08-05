# Use official Python slim image
FROM python:3.11-slim

# Prevent Python from writing .pyc files & enable stdout logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /code

# Install required system packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    build-essential \
    netcat-openbsd \
    pkg-config \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project files
COPY . .

# Collect static files (optional)
RUN python manage.py collectstatic --noinput || true

# Start Gunicorn server
CMD ["gunicorn", "sms.wsgi:application", "--bind", "0.0.0.0:8000"]
