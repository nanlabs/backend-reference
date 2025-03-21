# Base image with Python
FROM python:3.12-slim as builder

# Set the working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

FROM python:3.12-slim

# Copy built dependencies
COPY --from=builder /usr/lib/libgdal.so /usr/lib/libgdal.so
# Create non-root user
COPY --from=builder /etc/passwd /etc/passwd
USER appuser

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY transport.py .

# Run the script when the container starts
CMD ["python", "transport.py"]
