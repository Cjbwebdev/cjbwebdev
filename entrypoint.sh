#!/bin/bash
echo "Starting gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4
