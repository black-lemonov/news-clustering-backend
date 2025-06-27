FROM python:3.12.3

WORKDIR /app

COPY pyproject.toml ./

RUN pip install poetry && poetry install --no-root

COPY . .

CMD ["poetry", "run", "python", "src/main.py"]