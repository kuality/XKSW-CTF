FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      nginx \
      php8.3-fpm \
      ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN rm -f /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default \
 && rm -rf /var/www/html/*

COPY ./default /etc/nginx/conf.d/app.conf

COPY ./src/ /var/www/html/
RUN chown -R www-data:www-data /var/www \
 && find /var/www -type d -exec chmod 755 {} \;

EXPOSE 80
STOPSIGNAL SIGQUIT

CMD ["/bin/sh", "-c", "php-fpm8.3 -F & exec nginx -g 'daemon off;'"]
