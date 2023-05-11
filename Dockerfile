FROM python:3.10-bullseye as base

# Set environment variables
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base as builder

# install dependencies
RUN apt-get update
RUN apt-get install -y gcc musl-dev libpq-dev libffi-dev zlib1g-dev g++ libev-dev git build-essential \
    libev4 ca-certificates mailcap debian-keyring debian-archive-keyring apt-transport-https

RUN pip3 install -U pip
RUN pip3 install pipenv=="2023.4.20"

COPY Pipfile .
COPY Pipfile.lock .

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base as runtime

WORKDIR /usr/src/app/

COPY --from=builder /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN groupadd -g 1000 app && \
    useradd -r -u 1000 -g app app

RUN mkdir "/home/app"
RUN	chown -R app:app /home/app

COPY ./app /usr/src/app/
RUN	chown -R app:app /usr/src/app/
RUN chmod +x /usr/src/app/entrypoint.sh

USER app

EXPOSE 8080
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD [ "gunicorn", "main:app", "--workers", "8", "--worker-class", \
		"uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080" ]
