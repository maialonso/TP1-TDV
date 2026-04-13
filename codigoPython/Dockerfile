FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    make \
    g++ \
    && rm -rf /var/lib/apt/lists/*

CMD ["make"]