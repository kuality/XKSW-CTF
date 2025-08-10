FROM python:3.10-slim

WORKDIR /app

COPY app.py .
COPY flag.txt /app/flag.txt
RUN pip install flask

EXPOSE 8080

CMD ["python3", "app.py"]

