FROM fedora:34

LABEL name="semaphore/probe" \
      maintainer="Miroslav Jagelka <miro.jagelka@gmail.com>"

# Create non-root user
RUN adduser -u 10000 -g root colorsort

# Copy project into container
USER colorsort
ARG HOME_DIR=/tmp/colorsort/
RUN mkdir ${HOME_DIR}
COPY ./ ${HOME_DIR}
WORKDIR ${HOME_DIR}

# OpenCV library has dependencies that are installed automatically using
# dnf compared to pip3 where you need to install it separately
USER root
RUN dnf install -y python3-pip \
                   python3-opencv && \
    pip3 install -r requirements.txt
