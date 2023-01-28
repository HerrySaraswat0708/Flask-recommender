FROM python:3.11.0

RUN pip install Flask gunicorn

COPY server/src/ app/

WORKDIR /app

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 & app:app.py
