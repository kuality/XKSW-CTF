FROM php:8.2-apache
RUN a2enmod rewrite

COPY . /var/www/html/

RUN rm -rf /var/www/html/flag

COPY flag/grades.txt /flag/grades.txt

RUN chown root:www-data /flag/grades.txt \
 && chmod 640 /flag/grades.txt

EXPOSE 80

