# ==========================================
# Stage 1: Build the React Dashboard
# ==========================================
FROM node:22-alpine AS frontend-builder
WORKDIR /frontend

# Copy package manifests and install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy source code and build production bundle
COPY frontend/ ./
RUN npm run build

# ==========================================
# Stage 2: Unified Python Runtime
# ==========================================
FROM python:3.13-slim
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./backend/

# Copy compiled frontend from Stage 1
COPY --from=frontend-builder /frontend/dist ./frontend/dist

# Ensure persistent data directory exists
RUN mkdir -p /app/data

# Expose single unified port
EXPOSE 8000

# Run unified FastAPI + discord.py process
CMD ["python", "backend/app/main.py"]
