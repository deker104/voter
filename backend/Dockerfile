FROM python:3.10-alpine

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY . .

ENTRYPOINT [ "python", "server.py" ]
