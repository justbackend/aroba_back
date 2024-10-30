# Base image
FROM python:3.10-slim


# shell
SHELL ["/bin/bash", "-c"]
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

RUN apt-get update &&  apt-get -qy install gcc libjpeg-dev libxslt-dev libpq-dev libmariadb-dev \
    libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

# Install dependencies
COPY requirements/production.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Run migrations and start the server
