FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN useradd -m -s /bin/bash app && chown -R app:app /app
USER app

EXPOSE 8058

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8058", "--workers", "2", "--threads", "4"]
