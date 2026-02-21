FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias de sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3333

# Comando de inicio con Uvicorn (sin espacios extra)
CMD ["uvicorn", "V3_API:app", "--host", "0.0.0.0", "--port", "3333", "--workers", "1"]