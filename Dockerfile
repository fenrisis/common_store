
FROM python:3.10


WORKDIR /code

COPY pyproject.toml poetry.lock /code/


RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi


COPY . /code/


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
