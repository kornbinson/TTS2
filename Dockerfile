FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias de sistema necesarias para audio si hiciera falta
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3333

# Lanzamos con Uvicorn para máximo rendimiento asíncrono
CMD ["uvicorn", "V3_API:app", "--host", "0.0.0.0", "--port", "3333", "--workers", "1"]