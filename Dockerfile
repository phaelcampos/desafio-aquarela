FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

# Create the app user
RUN groupadd app && useradd -g app app

WORKDIR /app
COPY . .

RUN pip install poetry
RUN chmod +x entrypoint.sh
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
USER app

CMD poetry run uvicorn --host 0.0.0.0 desafio_aquarela.app:app --reload