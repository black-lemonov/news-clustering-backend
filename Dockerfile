FROM python:3.12-slim

WORKDIR /app


RUN pip install poetry


COPY pyproject.toml ./


RUN poetry config virtualenvs.create false && poetry install --no-root

RUN python -c "import nltk; nltk.download('punkt')"
RUN python -c "import nltk; nltk.download('stopwords')"
RUN python -c "import nltk; nltk.download('punkt_tab')"

COPY . ./

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]