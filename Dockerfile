# Use an official Python image as a base
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    UV_NO_INDEX=1 \
    UV_CACHE_DIR=/var/cache/uv

# Install uv package manager
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml ./
COPY . .

# Install dependencies using uv
# RUN uv sync

#COPY .env .env
ENV HF_HOME=/app/huggingface

# Set entrypoint command
CMD ["/app/run.sh"]