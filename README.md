## Build Hadoop Docker Image

```sh
docker build -t hadoop-app -f hadoop.Dockerfile .
```

<hr />

## Creating & Running Docker Container

```sh
docker run -p 8088:8088 --name hadoop-app -d hadoop-app
```

<hr />

## Accessing Hadoop in Docker Container

```sh
# start interactive shell in running container
docker exec -it hadoop-app bash

# once shell has started run hadoop "pi" example job
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.4.jar pi 10 100
```

<hr />

## Web interface of the Resource Manager

```text
http://localhost:8088
```

<hr />

## Get public IP adress for flask app using ngrok

```text
http://localhost:4040
```

<hr />
<br />

# Development setup

<hr />

### Create python virutal enviroment

Create and active virtual enviroment using venv library:

```sh
python3 -m venv .venv
source .venv/bin/activate (Linux)
.venv\Scripts\activate (Windows)
```

In some Windows cases before activating venv:

```sh
Set-ExecutionPolicy Unrestricted -Scope Process
```

<hr />

### Setup flask app

Linux/MacOS

```sh
export FLASK_APP=flaskr/run.py
```

Windows cmd

```sh
set FLASK_APP=flaskr/run.py
```

Windows powershell

```sh
$env:FLASK_APP = "flaskr/run.py"
```

Install app as library in development mode using setuptool

```sh
python -m pip install -e .[dev]
```

Build package (run command each time after changes anmd before building image from Dockerfile)

```sh
python setup.py bdist_wheel
```

<hr />

### Run flask app

```sh
flask run
```

<hr />

### Run unit tests

```sh
pytest tests
```

<hr />

### Run linter

Pytlint

```sh
python -m pylint flaskr/** tests/**
```

Black check

```sh
python -m black --check .
```

Black fix

```sh
python -m black .
```
