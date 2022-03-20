FROM python:3.8

ARG UID=1000
ARG GID=1000
ENV WORKDIR=/webapp/server

RUN mkdir /opt/linchfin \
  && apt update \
  && pip install --upgrade pip \
  && groupadd -g $GID linchfin \
  && useradd -g $GID -u $UID -d /home/linchfin -s /bin/bash linchfin

ADD requirements.txt /opt/linchfin/requirements.txt
RUN pip3 install -r /opt/linchfin/requirements.txt

ADD . $WORKDIR
WORKDIR $WORKDIR
USER linchfin
CMD ["uvicorn", "main:app", "--reload"]