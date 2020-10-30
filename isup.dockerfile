FROM python:2.7
EXPOSE 8000
WORKDIR /home/freshonions
ADD . /home/freshonions
RUN python2 -m pip install -r requirements.txt
RUN groupadd -r freshonions && useradd --no-log-init -r -g freshonions freshonions
USER freshonions
CMD init/isup-service.sh # to keep site status up to date
