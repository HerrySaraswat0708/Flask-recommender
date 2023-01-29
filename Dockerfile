FROM python:3

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install -r server/src/requirements.txt

EXPOSE 8000

CMD python ./app.py PORT --workers 1 --threads 8 & app:app
