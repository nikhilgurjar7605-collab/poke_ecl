# PokeEclipse Auto-Hunter Docker Image
# Enhanced for stability and cloud deployment
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Render/railway/cloud requirement)
EXPOSE 8080

# Set environment variables for stability
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8080
ENV HOST=0.0.0.0
ENV PYTHONFAULTHANDLER=1

# Prevent Python buffering for real-time logs
ENV PYTHONIOENCODING=utf-8

# Health check endpoint - ensures container stays alive
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Create non-root user for security (optional but recommended)
RUN useradd -m -u 1000 botuser || true
USER botuser || true

# Run the bot with proper signal handling
CMD ["python", "-m", "poke"]
