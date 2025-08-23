FROM php:8.2-apache

ARG DEBIAN_FRONTEND=noninteractive

RUN rm -rf /var/www/html/*

COPY . /var/www/html/

EXPOSE 80