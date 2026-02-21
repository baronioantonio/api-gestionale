FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080

# AVVIO CORRETTO (shell per espansione $PORT)
CMD sh -c "gunicorn -b 0.0.0.0:${PORT} app:app"