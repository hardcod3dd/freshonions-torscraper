FROM python:2.7
EXPOSE 8000
WORKDIR /home/freshonions
ADD . /home/freshonions
RUN apt update && apt install -y tor
RUN python2 -m pip install gunicorn
RUN python2 -m pip install -r requirements.txt
RUN groupadd -r freshonions && useradd --no-log-init -r -g freshonions freshonions
USER freshonions
CMD init/scraper-service.sh # to start crawling