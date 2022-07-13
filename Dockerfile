
FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive
ENV VERSION=1.7.0
RUN apt-get update
RUN apt-get install -y \
    python3 \
    python3-pip \
    unzip \
    wget \
    nano \
    vim \
    ffmpeg

# install chromium
RUN python3 -m pip install discord-webhooks
RUN python3 -m pip install discord-webhook
RUN python3 -m pip install argparse

COPY ./discord_chan.py /discord_chan.py

ENTRYPOINT ["python3", "/discord_chan.py"]
CMD ["-h"]
