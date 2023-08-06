FROM python:3.10-slim

WORKDIR /perm-300-app

ADD ./requirements.txt /perm-300-app/requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh