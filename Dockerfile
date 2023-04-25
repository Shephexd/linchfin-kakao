FROM python:3.8-slim

ARG UID=1000
ARG GID=1000
ARG WORKDIR=/webapp/server
ENV PORT=8080

RUN mkdir /opt/linchfin \
  && apt update \
  && apt install git nginx -y \
  && pip install --upgrade pip \
  && groupadd -g $GID linchfin \
  && useradd -g $GID -u $UID -d /home/linchfin -s /bin/bash linchfin

ENV NGINX_SET_REAL_IP_FROM="10.1.0.0/16"\
    PROXY_PASS="unix:/tmp/gunicorn.sock"\
    RESOURCE_DIR="$WORKDIR/resources"
ADD requirements.txt $WORKDIR/requirements.txt
RUN pip3 install -r $WORKDIR/requirements.txt

ADD . $WORKDIR
WORKDIR $WORKDIR
USER linchfin
CMD ["/bin/bash", "run.sh"]
