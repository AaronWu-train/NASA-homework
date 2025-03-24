docker container stop $(docker ps -a -q --filter="label=dnslab")
docker network rm dnslab-net
