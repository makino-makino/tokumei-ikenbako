FROM rust:buster

RUN apt-get update
RUN apt-get install -y gcc python3 python3-pip
RUN pip3 install flask sqlalchemy requests pycryptodome cerberus pytest

WORKDIR /api
CMD python3 serv.py &> &1
