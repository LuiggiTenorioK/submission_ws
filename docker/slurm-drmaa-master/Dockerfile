# syntax=docker/dockerfile:1

FROM rancavil/slurm-master:19.05.5-1

# Install slurm-drmaa
RUN apt-get update && apt-get install -y libslurm-dev python3.9 python3-pip python3-dev default-libmysqlclient-dev build-essential gunicorn

RUN wget https://github.com/natefoo/slurm-drmaa/releases/download/1.1.3/slurm-drmaa-1.1.3.tar.gz \
    && tar -xvzf slurm-drmaa-1.1.3.tar.gz \
    && cd slurm-drmaa-1.1.3 \
    && ./configure && make && make install && ldconfig 
