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
    libmariadb-dev-compat gettext cron openssh-client flake8 locales vim postgresql-client

# Upgrade pip
RUN pip install --upgrade pip

# Create the /opt/run directory
RUN mkdir -p /opt/run


# Set working directory
WORKDIR /aroba

# Copy requirements and install dependencies
COPY --chown=aroba:aroba requirements /aroba/requirements
RUN pip install -r requirements/production.txt

# Copy the rest of the project files
COPY --chown=aroba:aroba . .

# Add entrypoint.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN cron -f &


# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
