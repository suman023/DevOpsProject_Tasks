# Use lightweight Python image
FROM python:3.9-alpine

# Set working directory inside container
WORKDIR /app

# Copy dependency file first (for layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Copy HTML and CSS templates 
COPY templates ./templates
COPY static ./static

# Expose application port
EXPOSE 80

# Start application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]


