# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set work directory
WORKDIR /app

# Install system dependencies needed for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv $VIRTUAL_ENV

# Install uv for faster package management
RUN pip install uv

# Copy requirements and project files
COPY pyproject.toml README.md docker-requirements.txt ./

# Install dependencies from docker-requirements.txt into the virtual environment
RUN uv pip install -r docker-requirements.txt

# Stage 2: Runtime image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set work directory
WORKDIR /app

# Install only runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ca-certificates \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
COPY --from=builder /app/venv /app/venv

# Copy the entire poe package
COPY poe /app/poe/

# Copy API package
COPY packages/your-api /app/packages/your-api/

# Expose port
EXPOSE 8000

# Run Django server
CMD ["sh", "-c", "cd packages/your-api && python manage.py migrate && python manage.py collectstatic --no-input && python manage.py runserver 0.0.0.0:8000"] 