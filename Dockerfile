FROM python:3.12-slim

# directory di lavoro nel container
WORKDIR /app

# copia requirements e installa dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copia tutto il codice
COPY . .

# espone la porta Flask
EXPOSE 8080

# comando di avvio
CMD ["python", "app.py"]