# Base image
FROM python:3.10-slim

# shell
SHELL ["/bin/bash", "-c"]

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Paket ro'yxatini yangilang va kerakli kutubxonalarni o'rnating
RUN apt-get update && \
    apt-get -qy install gcc libjpeg-dev libxslt-dev libpq-dev libmariadb-dev \
    libmariadb-dev-compat gettext cron openssh-client locales vim postgresql-client-16 nano

# Upgrade pip
RUN pip install --upgrade pip

# Create the /opt/run directory
RUN mkdir -p /opt/run


# Set working directory
WORKDIR /aroba
COPY requirements requirements/

# Copy requirements and install dependencies
RUN pip install -r requirements/production.txt

# Copy the rest of the project files
COPY . .

# Add entrypoint.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN cron -f &



