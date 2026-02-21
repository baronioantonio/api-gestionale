FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Railway espone PORT dinamico
ENV PORT=8080

# AVVIO CORRETTO PER RAILWAY
CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "app:app"]