docker stop `docker ps -a -q`
docker rm `docker ps -a -q`
docker rmi $(docker images | awk '/^<none>/ { print $3 }')
