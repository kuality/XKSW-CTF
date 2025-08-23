FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir selenium flask

RUN useradd -m me2nuk

COPY ./flag.txt /src/flag.txt

COPY --chown=root:root ./src /src

WORKDIR /src

EXPOSE 8080

ENTRYPOINT ["python3", "/src/app.py"]