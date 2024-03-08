FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry --no-cache-dir && poetry config virtualenvs.create false && poetry install --without dev

COPY . /app
