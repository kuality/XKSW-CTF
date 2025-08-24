FROM ubuntu:22.04@sha256:3d1556a8a18cf5307b121e0a98e93f1ddf1f3f8e092f1fddfd941254785b95d7

ENV user pwn

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
      python3 socat ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos "" -u 1337 $user

ADD ./flag /flag
ADD ./prob /home/$user/prob
ADD ./bridge.py /home/$user/bridge.py

RUN chown root:$user /flag /home/$user/prob /home/$user/bridge.py && \
    chmod 440 /flag && \
    chmod 550 /home/$user/prob /home/$user/bridge.py

WORKDIR /home/$user
USER $user
EXPOSE 1004

CMD socat TCP-LISTEN:1004,reuseaddr,fork,keepalive,linger=1 \
    EXEC:"python3 /home/pwn/bridge.py",pty,setsid,stderr
