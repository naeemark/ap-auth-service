FROM python:3.8.3-slim

RUN mkdir /app
WORKDIR /app

COPY Pip* /app/

RUN pip install --upgrade pip && \
  pip install pipenv && \
  pipenv install --system --deploy --ignore-pipfile

ADD . /app

EXPOSE $FLASK_RUN_PORT

CMD gunicorn --chdir src app:app -w 2 --threads 2 -b 0.0.0.0:${FLASK_RUN_PORT}
