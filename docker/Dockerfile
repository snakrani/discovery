#
# See: https://github.com/docker-library/python/blob/master/2.7/stretch/slim/Dockerfile
#
FROM python:2.7-slim-stretch

#
# Container environment variables
#
ENV PATH /venv/bin:$PATH
ENV PYTHONUNBUFFERED 1

#
# Project directory
#
RUN mkdir /discovery
VOLUME /discovery
WORKDIR /discovery

#
# Application requirements
#
COPY ./scripts/setup-python.sh /usr/local/discovery/bin/setup-python.sh
COPY ./requirements.txt /usr/local/discovery/requirements.txt
COPY ./requirements-test.txt /usr/local/discovery/requirements-test.txt

RUN /usr/local/discovery/bin/setup-python.sh /dev/stderr \
    && rm -rf /tmp/*

#
# Javascript dependencies
#
COPY ./scripts/setup-phantomjs.sh /usr/local/discovery/bin/setup-phantomjs.sh

RUN /usr/local/discovery/bin/setup-phantomjs.sh /dev/stderr \
    && rm -rf /tmp/*
