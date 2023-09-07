FROM python:3.10

RUN mkdir -m 777 /app

RUN pip install poetry
COPY ./.env ./poetry.lock ./pyproject.toml /app/

WORKDIR /app/

COPY . .

RUN poetry --no-root install

ENTRYPOINT ["poetry", "run", "uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0"]