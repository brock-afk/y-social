FROM python:3.11.4-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip
RUN pip install poetry==1.5.1

COPY . /app/

RUN poetry install --sync

ENTRYPOINT [ "poetry", "run" ]

EXPOSE 8000

CMD ["gunicorn", "y_social.server.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]