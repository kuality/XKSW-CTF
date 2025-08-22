FROM ubuntu:24.04

RUN apt update
RUN apt install python3 python3-pip chromium-chromedriver -y
RUN python3 -m pip install selenium flask

RUN useradd -m me2nuk

COPY ./flag.txt /src/flag.txt

COPY --chown=root:root ./src /src

WORKDIR /src

EXPOSE 8080

ENTRYPOINT ["python3", "/src/app.py"]