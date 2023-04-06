# syntax=docker/dockerfile:1

FROM slurm-drmaa-master

COPY config.json /
COPY compose_entrypoint.sh /
RUN chmod +x /compose_entrypoint.sh

RUN pip3 install https://github.com/damiclem/submission_lib/archive/setup.zip
RUN pip3 install https://github.com/LuiggiTenorioK/submission_ws/archive/main.zip
# RUN cd / && git clone https://github.com/LuiggiTenorioK/submission_ws.git && cd submission_ws && pip3 install -r requirements.txt

CMD submission-ws