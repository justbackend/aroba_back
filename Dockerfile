# Base image
FROM python:3.10-slim

# shell
SHELL ["/bin/bash", "-c"]

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Update package list and install dependencies
RUN apt-get update && \
    apt-get -qy install gcc libjpeg-dev libxslt-dev libpq-dev libmariadb-dev \
    libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

# Upgrade pip
RUN pip install --upgrade pip

# Create the /opt/run directory
RUN mkdir -p /opt/run

# Create a user
RUN useradd -rms /bin/bash aroba && chmod 777 /opt/run

# Set working directory
WORKDIR /aroba

# Create directories for media and static files
RUN mkdir /aroba/media/ && mkdir /aroba/static && chown -R aroba:aroba /aroba && chmod 755 /aroba

# Copy project files
COPY --chown=aroba:aroba . .

# Install dependencies
RUN pip install -r requirements/production.txt

# Switch to the created user
USER aroba

# Run migrations and start the server
CMD ["gunicorn", "-b", "0.0.0.0:8000", "core.wsgi:application"]
