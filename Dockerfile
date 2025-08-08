# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
Pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Command to run the app
CMD ["streamlit", "run", "app.py"]