# pull official base image
FROM python:3.10.8-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1   #Prevents Python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1          #Prevents Python from buffering stdout and stderr

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .