# Commands to run

1. $docker build . --tag=dj_docker
2. $docker run -d -p 7999:6060 --name=container_dj_docker dj_docker

Warning: This version doesn't have psycopg2 support!
