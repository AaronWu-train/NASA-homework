FROM ubuntu:22.04

RUN apt-get update \
  && apt-get install -y \
  bind9 \
  bind9utils \
  bind9-doc \
  dnsutils \
  vim	\
  net-tools 


# Enable IPv4
#RUN sed -i 's/OPTIONS=.*/OPTIONS="-4 -u bind"/' /etc/default/bind9

RUN test -f /etc/default/bind9 || echo 'OPTIONS=""' > /etc/default/bind9 \
    && sed -i 's/OPTIONS=.*/OPTIONS="-4 -u bind"/' /etc/default/bind9

# Copy configuration files
COPY named.conf.options /etc/bind/
COPY named.conf.local /etc/bind/
COPY name.hosts /etc/bind/zones/
COPY name.rev1 /etc/bind/zones/

