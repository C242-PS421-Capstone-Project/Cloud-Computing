FROM python:3.12-slim

# Install missing OpenGL libs for opencv
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /usr/src/app

# Copy the local code to the container's working directory
COPY . .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask application
EXPOSE 5000

# Set Flask app entry point and bind it to 0.0.0.0
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
