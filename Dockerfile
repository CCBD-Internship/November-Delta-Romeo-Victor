FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN apt-get install -y gunicorn
RUN apt-get install -y python-gevent
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
LABEL creators="the NVRD team"