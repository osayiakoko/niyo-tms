# Use an official Python runtime as the base image
FROM python:3.11.8-bullseye

# Set the working directory in the container
WORKDIR /opt/project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .

# Install dependencies
RUN set -xe \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install virtualenvwrapper poetry==1.7.1 gunicorn uvicorn[standard] \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY ["poetry.lock", "pyproject.toml", "./"]
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# Copy project files
COPY ["Makefile", "./"]
COPY src src

# Expose the Django development server port (adjust if needed)
EXPOSE 8000

# Set up the entrypoint
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
