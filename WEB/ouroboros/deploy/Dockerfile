FROM php:8.2-apache

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN docker-php-ext-install mysqli

RUN rm -rf /var/www/html/*

COPY app /var/www/html/

EXPOSE 80