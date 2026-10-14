
FROM python:3.11-slim

WORKDIR /app

# Install PostgreSQL build dependencies and curl for health checks
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Render provides PORT; use 10000 as local/default fallback
EXPOSE 10000

# Start Streamlit on Render's assigned port
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-10000} --server.address=0.0.0.0"]
