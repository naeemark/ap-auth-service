FROM python:3.8.3-slim

RUN mkdir /app
WORKDIR /app

COPY Pip* /app/

RUN pip install --upgrade pip && \
  pip install pipenv && \
  pipenv install --system --deploy --ignore-pipfile

ADD . /app

EXPOSE $FLASK_RUN_PORT

CMD flask run --host=0.0.0.0
