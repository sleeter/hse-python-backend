FROM python:3.12-slim

ARG PYTHONFAULTHANDLER=1
ARG PYTHONHASHSEED=random
ARG PIP_NO_CACHE_DIR=on
ARG PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR ./app

RUN apt update && apt install make

RUN pip install poetry
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-root

COPY . .

ENV PYTHONPATH="/app"
EXPOSE 8000
CMD ["poetry", "run", "python", "hw_2/main.py"]