FROM python:3.9-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install system dependencies for pygame & X11
RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libgl1 \
    libgl1-mesa-dri \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxrandr2 \
    libxcursor1 \
    libxfixes3 \
    libxi6 \
    libxss1 \
    libxtst6 \
    && rm -rf /var/lib/apt/lists/*

# Force software rendering for compatibility
ENV LIBGL_ALWAYS_SOFTWARE=1
ENV SDL_VIDEODRIVER=x11

# Set working directory first
WORKDIR /app

# Copy requirements and install (better layer caching)
COPY requirements.txt .
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

CMD ["python3", "snake.py"]
