FROM debian
EXPOSE 9050
EXPOSE 8118
EXPOSE  3128
RUN apt update && apt install -y tor privoxy squid
WORKDIR /home/freshonions
ADD . /home/freshonions
COPY etc/privoxy.config.default /etc/privoxy/config
COPY etc/squid.conf /etc/squid/squid.conf
CMD /etc/init.d/tor start && /etc/init.d/squid stqrt && privoxy --no-daemon /etc/privoxy/config
