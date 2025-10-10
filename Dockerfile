# Use slim Python image
FROM python:3.11-slim

# Avoid tz/locale prompts during apt
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# System deps required by Tesseract & OpenCV
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      tesseract-ocr libtesseract-dev \
      libgl1 libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Tell pytesseract where the binary is (Linux)
ENV TESSERACT_CMD=/usr/bin/tesseract
# (If your code uses pytesseract directly, this is enough.)
# You can also set it in code: pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Start your bot
CMD ["python", "bot.py"]
