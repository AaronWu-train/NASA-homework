docker build -t host .
docker run -dit --rm --name=host1 --label=dnslab --net=dnslab-net --dns=172.20.0.2  --ip=172.20.0.3 --mount type=bind,source=$(pwd)/resolv.conf,target=/etc/resolv.conf host
docker exec -it host1 bash
