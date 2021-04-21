FROM ubuntu:18.04

ADD . /code/
WORKDIR /code

RUN apt-get update && \
  apt-get install -y software-properties-common && \
  add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update

RUN apt-get install -y build-essential python3.7 python3.7-dev python3-pip python3.7-venv nginx supervisor openssl
RUN apt-get install -y git
RUN apt-get install libssl-dev

RUN python3.7 -m pip install -U pip
RUN python3.7 -m pip install wheel

RUN CFLAGS="-I/usr/local/opt/openssl/include" LDFLAGS="-L/usr/local/opt/openssl/lib" \
  UWSGI_PROFILE_OVERRIDE=ssl=true pip3 install uwsgi -Iv

RUN python3.7 -m pip install -r requirements.txt

RUN mkdir -p /var/log/uwsgi

COPY uwsgi.ini /etc/uwsgi/

COPY nginx.conf /etc/nginx/

COPY nginx.conf /etc/nginx/conf.d/

COPY supervisord.conf /etc/supervisord.conf

ENV PYTHONPATH=/code

CMD /usr/bin/supervisord -c /etc/supervisord.conf
