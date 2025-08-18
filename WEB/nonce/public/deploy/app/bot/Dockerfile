FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir selenium flask

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

RUN useradd --password=toor -m me2nuk

COPY . /app/
WORKDIR /app

USER me2nuk

EXPOSE 8080

ENTRYPOINT ["python3", "app.py"]