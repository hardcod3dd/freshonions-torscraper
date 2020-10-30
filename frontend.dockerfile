FROM python:2.7
EXPOSE 8080
WORKDIR /home/freshonions
ADD . /home/freshonions
RUN python2 -m pip install -r requirements.txt
RUN groupadd -r freshonions && useradd --no-log-init -r -g freshonions freshonions
USER freshonions
CMD sh scripts/web.sh
