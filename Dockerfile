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

# Create a user
RUN useradd -rms /bin/bash aroba && chmod 777 /opt/run

# Set working directory
WORKDIR /aroba

# Create directories for media and static files
RUN mkdir -p /aroba/media/ /aroba/static /aroba/staticfiles && \
    chmod -R 777 /aroba/media /aroba/static /aroba/staticfiles && \
    chown -R aroba:aroba /aroba/media /aroba/static /aroba/staticfiles

# Copy only the requirements directory and install dependencies
COPY --chown=aroba:aroba requirements /aroba/requirements
RUN pip install -r requirements/production.txt

# Copy the rest of the project files
COPY --chown=aroba:aroba . .

# Switch to the created user
USER aroba

# Run migrations and start the server
CMD ["gunicorn", "-b", "0.0.0.0:8001", "core.wsgi:application"]
