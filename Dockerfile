FROM alpine:latest 
MAINTAINER theydonthaveit "theydonthaveit@gmail.com"

ENV APP_DIR /app
COPY ./app ${APP_DIR}

RUN apk update && \
    apk add python python3 python3-dev supervisor && \
    pip3 install --upgrade pip && \
    pip3 install --trusted-host pypi.python.org -r /app/requirements.txt && \
    mkdir -p /etc/supervisor && \
    mkdir -p ${APP_DIR}/web && \
    mkdir -p ${APP_DIR}/conf && \
    mkdir -p ${APP_DIR}/logs && \
    cat ${APP_DIR}/conf/*.ini >> /etc/supervisor/supervisord.conf

COPY ./app ${APP_DIR}
VOLUME ["${APP_DIR}"]
EXPOSE 4000
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
