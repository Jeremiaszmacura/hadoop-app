FROM ubuntu:20.04

RUN apt-get update

RUN apt-get install -y curl

RUN apt purge gnupg2 && apt autoremove && apt autoclean && apt install -y gnupg2

RUN apt-get install -y ca-certificates

RUN sh -c 'curl -s --location https://www.mongodb.org/static/pgp/libmongocrypt.asc | gpg --dearmor >/etc/apt/trusted.gpg.d/libmongocrypt.gpg'

RUN echo "deb https://libmongocrypt.s3.amazonaws.com/apt/ubuntu focal/libmongocrypt/1.5 universe" | tee /etc/apt/sources.list.d/libmongocrypt.list

RUN apt-get update

RUN apt-get install -y libmongocrypt