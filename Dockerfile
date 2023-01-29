FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]PORT --workers 1 --threads 8 & app:app