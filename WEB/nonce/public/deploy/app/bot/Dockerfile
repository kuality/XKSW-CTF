FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir selenium flask

# Chrome 및 ChromeDriver 환경 변수 설정
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV CHROMEDRIVER_WHITELISTED_IPS=""
ENV CHROMEDRIVER_LOG_LEVEL=0

# ARM64 아키텍처 호환성을 위한 추가 설정
ENV CHROME_HEADLESS=1
ENV CHROME_NO_SANDBOX=1
ENV CHROME_DISABLE_DEV_SHM_USAGE=1

RUN useradd --password=toor -m me2nuk

COPY . /app/
WORKDIR /app

USER me2nuk

EXPOSE 8080

ENTRYPOINT ["python3", "app.py"]