FROM debian:stretch-slim

#
# Container environment variables
#
ENV PATH /venv/bin:$PATH
ENV LANG C.UTF-8
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
COPY ./requirements-dev.txt /usr/local/discovery/requirements-dev.txt

RUN /usr/local/discovery/bin/setup-python.sh /dev/stderr \
    && rm -rf /tmp/*

#
# Initial command
#
CMD ["python3"]
