FROM python:3.9 as backend

WORKDIR /requirements
COPY requirements.txt /requirements
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN apt-get -y update
RUN apt-get install -y ffmpeg
RUN apt-get install -y libopus-dev

WORKDIR /bigboy
COPY ./ /bigboy