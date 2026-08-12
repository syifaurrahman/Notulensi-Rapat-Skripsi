# ============================================================
# Dockerfile.php — Container untuk Web PHP (Apache)
# ============================================================
FROM php:8.2-apache

# Install ekstensi PHP yang dibutuhkan
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libcurl4-openssl-dev \
    zip \
    unzip \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install mysqli pdo pdo_mysql gd curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Aktifkan mod_rewrite Apache (untuk .htaccess)
RUN a2enmod rewrite

# Konfigurasi Apache agar .htaccess bisa override
RUN sed -i 's/AllowOverride None/AllowOverride All/g' /etc/apache2/apache2.conf

# Salin semua file PHP ke folder web Apache
COPY . /var/www/html/

# Set permission folder agar Apache bisa tulis hasil transkripsi
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html \
    && mkdir -p /var/www/html/hasil \
    && mkdir -p /var/www/html/hasil_summarize/Lexrank \
    && mkdir -p /var/www/html/hasil_summarize/Ollama \
    && chmod -R 777 /var/www/html/hasil \
    && chmod -R 777 /var/www/html/hasil_summarize

EXPOSE 80
