FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Pygame
# - xvfb: Virtual display for headless fallback
# - vim: Useful for debugging
# - curl: For testing connectivity
RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libportmidi0 \
    libfreetype6 \
    xvfb \
    vim \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install dev tools (optional but handy)
RUN pip install ipython debugpy

# Copy game code
COPY snake.py .

# Copy entrypoint and make executable
COPY scripts/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["python", "-u", "snake.py"]

EXPOSE 5678
