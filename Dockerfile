FROM fedora:latest

ARG HOME_DIR=/tmp/colorsort/

RUN mkdir ${HOME_DIR}
COPY ./ ${HOME_DIR}
WORKDIR ${HOME_DIR}
RUN mkdir colors

# OpenCV library has dependencies that are installed automatically using
# dnf compared to pip3 where you need to install it separately
RUN dnf install -y python3-pip \
                   python3-opencv && \
    pip3 install -r requirements.txt
