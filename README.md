## Build Hadoop Docker Image

```sh
docker build -t hadoop-app .
```

## Creating & Running Docker Container

```sh
docker run -p 8088:8088 --name hadoop-app-container -d hadoop-app
```

## Accessing Hadoop in Docker Container

```sh
# start interactive shell in running container
docker exec -it hadoop-app-container bash

# once shell has started run hadoop "pi" example job
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.4.jar pi 10 100
```

## Web interface of the Resource Manager

```text
http://localhost:8088
```