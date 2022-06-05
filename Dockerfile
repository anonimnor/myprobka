#syntax=docker/dockerfile:1

FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow
WORKDIR /code

COPY . .
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip install -r requirements.txt
RUN pip install lxml \ requests \ pillow
RUN apt update

RUN apt install mc -y
RUN apt install htop -y
