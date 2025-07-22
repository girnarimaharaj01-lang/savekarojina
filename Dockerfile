# Step 1: Use Python 3.10 or higher
FROM python:3.10-slim-bullseye

# Step 2: Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ffmpeg \
    wget \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Step 3: Set working directory
WORKDIR /app

# Step 4: Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -U -r requirements.txt

# Install Gunicorn for production
RUN pip install gunicorn

# Step 5: Copy the rest of the code
COPY . .

# Step 6: Expose port
EXPOSE 5000

# Step 7: Start the app with Gunicorn and the main bot script
CMD gunicorn app:app --bind 0.0.0.0:5000 & python3 main.py
