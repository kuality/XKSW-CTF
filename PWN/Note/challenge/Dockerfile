FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive\
    LC_CTYPE=C.UTF-8

# 포트 설정
EXPOSE 1004

# 레포지토리 변경
RUN sed -i "s/archive.ubuntu/mirror.kakao/g" /etc/apt/sources.list

# 업데이트
RUN apt update && apt upgrade -y
RUN apt install -y xinetd ssh
RUN apt install -y --no-install-recommends tzdata
# -----------------------------------------------
RUN apt-get install -y socat
RUN apt-get install -y qemu-system

# 타임존 설정
RUN echo "Asia/Seoul" > /etc/timezone
RUN rm -f /etc/localtime
RUN dpkg-reconfigure --frontend noninteractive tzdata

# 서비스 설정
RUN touch /var/log/prob.log
RUN touch /etc/xinetd.d/prob
RUN echo "service prob                         " >> /etc/xinetd.d/prob
RUN echo "{                                       " >> /etc/xinetd.d/prob
RUN echo "    flags = REUSE                       " >> /etc/xinetd.d/prob
RUN echo "    disable = no                        " >> /etc/xinetd.d/prob
RUN echo "    socket_type = stream                " >> /etc/xinetd.d/prob
RUN echo "    wait = no                           " >> /etc/xinetd.d/prob
RUN echo "    user = pwn                          " >> /etc/xinetd.d/prob
RUN echo "    server = /home/pwn/run.sh         " >> /etc/xinetd.d/prob
RUN echo "    port = 1004                        " >> /etc/xinetd.d/prob
RUN echo "    protocol = tcp                      " >> /etc/xinetd.d/prob
RUN echo "    log_type = FILE /var/log/prob.log" >> /etc/xinetd.d/prob
RUN echo "    log_on_success = HOST DURATION EXIT " >> /etc/xinetd.d/prob
RUN echo "}                                       " >> /etc/xinetd.d/prob
RUN echo "prob 1004/tcp" >> /etc/services


# 계정 설정
RUN useradd pwn -m -s /bin/bash
RUN echo "pwn:v1u2nk33y!" | chpasswd
RUN echo "root:v1u2nk33y!root" | chpasswd

# ASLR 설정
RUN touch /etc/sysctl.d/01-disable-aslr.conf
RUN echo "kernel.randomize_va_space = 2" >> /etc/sysctl.d/01-disable-aslr.conf

# 기본 권한 설정
RUN chmod -R 700 /bin
RUN chmod -R 700 /sbin
RUN chmod -R 700 /usr/bin
RUN chmod -R 700 /usr/sbin
RUN chmod 755 /bin
RUN chmod 755 /sbin
RUN chmod 755 /usr/bin
RUN chmod 755 /usr/sbin
RUN chmod 755 /bin/ls
RUN chmod 755 /bin/cat
RUN chmod 755 /bin/sh
RUN chmod 755 /bin/dash
RUN chmod 755 /bin/bash
RUN chmod 600 /etc/passwd
RUN chmod 600 /etc/passwd-
RUN chmod 600 /etc/group
RUN chmod 600 /etc/group-
RUN chmod 600 /etc/shadow
RUN chmod 600 /etc/shadow-
RUN chmod -R 700 /var/log
RUN chmod -R 700 /var/tmp
RUN chmod 700 /var
RUN chmod 700 /tmp
RUN chmod 600 /dev/shm
# --------------------

# 바이너리 복사
COPY run.sh /home/pwn/run.sh
COPY bzImage /home/pwn/bzImage
COPY initramfs.cpio.gz /home/pwn/initramfs.cpio.gz

RUN chmod 755 /home/pwn/run.sh /usr/bin/qemu-system-x86_64 /home/pwn/bzImage
RUN chown pwn:pwn /home/pwn/run.sh /home/pwn
RUN chmod +x /home/pwn/bzImage

# 홈 디렉토리 설정
RUN rm -rf /home/pwn/.bash_history
RUN rm -rf /home/pwn/.bash_logout
RUN rm -rf /home/pwn/.bashrc
RUN rm -rf /home/pwn/.profile
RUN rm -rf /home/pwn/.cache
RUN ln -s /dev/null /home/pwn/.bash_history
RUN ln -s /dev/null /home/pwn/.bash_logout
RUN ln -s /dev/null /home/pwn/.bashrc
RUN ln -s /dev/null /home/pwn/.profile
RUN ln -s /dev/null /home/pwn/.cache

RUN chown pwn.pwn /home/pwn/.bash_history
RUN chown pwn.pwn /home/pwn/.bash_logout
RUN chown pwn.pwn /home/pwn/.bashrc
RUN chown pwn.pwn /home/pwn/.profile
RUN chown pwn.pwn /home/pwn/.cache
# -------------------------------------
RUN chown pwn.pwn /home/pwn
RUN chown pwn.pwn /home/pwn/run.sh

CMD ["/usr/sbin/xinetd","-dontfork"]
