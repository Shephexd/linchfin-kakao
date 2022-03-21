FROM python:3.8

ARG UID=1000
ARG GID=1000
ARG WORKDIR=/webapp/server
ENV PORT=80

RUN mkdir /opt/linchfin \
  && apt update \
  && pip install --upgrade pip \
  && groupadd -g $GID linchfin \
  && useradd -g $GID -u $UID -d /home/linchfin -s /bin/bash linchfin

ADD requirements.txt $WORKDIR/requirements.txt
RUN pip3 install -r $WORKDIR/requirements.txt

ADD . $WORKDIR
WORKDIR $WORKDIR
USER linchfin
CMD ["/bin/bash", "run.sh"]