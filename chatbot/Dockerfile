FROM python:3.9-slim

# Instalacja zależności
RUN pip install pika

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie plików aplikacji do kontenera
COPY . .

# Uruchomienie aplikacji
CMD [ "python", "worker.py" ]
