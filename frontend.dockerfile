FROM python:3.10.0b4
EXPOSE 8080
WORKDIR /home/freshonions
ADD . /home/freshonions
RUN pip install -r requirements_frontend.txt
RUN groupadd -r freshonions && useradd --no-log-init -r -g freshonions freshonions
USER freshonions
CMD sh scripts/web.sh
