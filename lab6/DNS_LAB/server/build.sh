docker network create --subnet=172.20.0.0/16 dnslab-net
docker build -t bind9 .
docker run -dit --rm  --name=dns-server --label=dnslab --net=dnslab-net --dns=172.20.0.2 --ip=172.20.0.2 --mount type=bind,source=$(pwd)/resolv.conf,target=/etc/resolv.conf bind9 
#docker exec -d dns-server /etc/init.d/bind9 start
docker exec -d dns-server named -4 -u bind
docker attach dns-server

