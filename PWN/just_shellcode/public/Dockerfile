FROM ubuntu:22.04@sha256:3d1556a8a18cf5307b121e0a98e93f1ddf1f3f8e092f1fddfd941254785b95d7

ENV user pwn
ENV prob_port 1004

RUN apt-get update
RUN apt-get -y install socat

RUN adduser -u 1337 $user

ADD ./flag /flag
ADD ./prob /home/$user/prob

RUN chown root:$user /flag
RUN chown root:$user /home/$user/prob

RUN chmod +x /home/$user/prob
RUN chmod 440 /flag

WORKDIR /home/$user
USER $user
EXPOSE $prob_port

CMD socat TCP-L:1004,reuseaddr,fork, EXEC:"./prob"
