# Step 1: Python ka version 3.10 ya usse upar ka istemal karein
FROM python:3.10-slim-bullseye

# Step 2: Zaroori packages install karein
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ffmpeg \
    wget \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Step 3: Working directory set karein
WORKDIR /app

# Step 4: requirements.txt ko copy karke install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -U -r requirements.txt

# Gunicorn ko install karein (production server ke liye)
RUN pip install gunicorn

# Step 5: Baaki saare code ko copy karein
COPY . .

# Step 6: Port expose karein
EXPOSE 5000

# Step 7: Application ko Gunicorn aur main bot script ke saath start karein
# Yeh Gunicorn web server ko background mein chalayega aur main.py ko foreground mein
CMD gunicorn app:app --bind 0.0.0.0:5000 & python3 main.py
