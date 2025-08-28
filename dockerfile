FROM docker.io/python:3.12-slim

ARG BASE_DIR=/opt/app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y curl build-essential libpq-dev \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR ${BASE_DIR}
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-ansi

WORKDIR ${BASE_DIR}/src
COPY ./src ./

RUN SECRET_KEY=empty python3 ./manage.py collectstatic --noinput

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]


