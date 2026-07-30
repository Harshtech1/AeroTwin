# --- Development Stage ---
FROM python:3.12-slim-bullseye AS development

WORKDIR /workspace/backend

# Install system dependencies (build-essential needed for compiling certain packages, libpq-dev for PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY . .

# Run FastAPI app via uvicorn with hot-reloading
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
