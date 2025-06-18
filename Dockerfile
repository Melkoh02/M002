# Use the official Python 3.10 image from Docker Hub
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install Poetry
RUN pip install poetry

# Copy the project metadata (including README) into the container
COPY pyproject.toml poetry.lock* README.md /code/

# Configure Poetry and install dependencies (skip installing the root project)
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

# Install GDAL and related dependencies
RUN apt-get update \
    && apt-get install -y binutils gdal-bin libproj-dev libgdal-dev build-essential cron
RUN pip install gdal==`gdal-config --version`

RUN mkdir -p /code/static \
    && chmod -R 755 /code/static

# Copy the rest of the project
COPY . /code/

# Run the collectstatic command
RUN python manage.py collectstatic --noinput

# Run the image as a non-root user
RUN adduser --disabled-password --gecos "" django
USER django
