FROM python:3.5

ENV PYTHONUNBUFFERED 1

RUN set x; \
        apt-get update \
        && apt-get install -y binutils \
        libproj-dev \
        gdal-bin

RUN mkdir -p /root/.ssh

RUN mkdir -p /phr/static

COPY .ssh /root/.ssh

COPY . /

VOLUME ["/phr/static"]

RUN pip install -r requirements/prod.txt

ENV ALLOWED_HOSTS *
ENV SECRET_KEY xxxxxx 
ENV DJANGO_SETTINGS_MODULE config.settings.prod
ENV DB_NAME postgres
ENV DB_PASSWORD postgres
ENV LOGIN_DOMAIN .minsa.gob.pe
ENV DB_HOST db
ENV DB_PORT 5432
ENV DB_USER postgres

EXPOSE 8000
