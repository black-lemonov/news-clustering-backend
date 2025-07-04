FROM python:3.12-slim

WORKDIR /app


RUN pip install poetry


COPY pyproject.toml ./

RUN apt-get update && apt-get install -y libpq-dev gcc

RUN poetry config virtualenvs.create false && poetry install --no-root

RUN python -c "import nltk; nltk.download('punkt')"
RUN python -c "import nltk; nltk.download('stopwords')"
RUN python -c "import nltk; nltk.download('punkt_tab')"

COPY . ./

RUN apt-get update && apt-get install -y supervisor

RUN mkdir -p /var/log/supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["bash", "start-dev.sh"]