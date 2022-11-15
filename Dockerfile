FROM python:3.10.8-bullseye as builder

WORKDIR /build

# install dependencies
RUN apt-get update
RUN apt-get install -y gcc musl-dev libpq-dev libffi-dev zlib1g-dev g++ libev-dev git build-essential

RUN pip3 install -U pip

COPY ./requirements.txt ./
RUN pip3 wheel \
		--no-cache-dir \
		--wheel-dir wheels \
		-r requirements.txt

FROM python:3.10.8-bullseye

# Set environment variables.
ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY --from=builder /build/wheels /wheels

RUN apt-get update
RUN apt-get install -y libev4 ca-certificates mailcap debian-keyring debian-archive-keyring apt-transport-https

WORKDIR /usr/src/app/

RUN groupadd -g 1000 app && \
    useradd -r -u 1000 -g app app

RUN mkdir "/home/app"
RUN	chown -R app:app /home/app
RUN	chown -R app:app /wheels

RUN pip install -U pip
RUN pip install --no-cache /wheels/*

COPY ./app /usr/src/app/
RUN	chown -R app:app /usr/src/app/
RUN chmod +x /usr/src/app/entrypoint.sh

USER app

EXPOSE 8080
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD [ "gunicorn", "main:app", "--workers", "8", "--worker-class", \
		"uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080" ]
