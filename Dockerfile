# Base image
FROM python:3.10-slim


# shell
SHELL ["/bin/bash", "-c"]
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /aroba

RUN apt-get update &&  apt-get -qy install gcc libjpeg-dev libxslt-dev libpq-dev libmariadb-dev \
    libmariadb-dev-compat gettext cron openssh-client flake8 locales vim \

RUN pip install --upgrade pip

RUN useradd -rms /bin/bash aroba &&  chmod 777 /opt/run

# Copy project files
COPY . .

# Install dependencies
RUN pip install -r requirements/production.txt

# Run migrations and start the server

