# Use lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variable (Render will inject BOT_TOKEN)
ENV PORT=10000
EXPOSE 10000

# Run bot
CMD ["python", "bot.py"]