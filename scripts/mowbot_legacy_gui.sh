#!/bin/bash

IMAGE_NAME="ghcr.io/serene4mr/mowbot_legacy_gui:latest"

xhost +local:docker
export DISPLAY=:0

docker run -i --rm \
  --name mowbot_legacy_gui \
  --net host \
  --privileged \
  -v /dev:/dev \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /home/mowbot/mowbot_legacy_data:/mowbot_legacy_data \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e DISPLAY=$DISPLAY \
  -e HOST_HOME=$HOME \
  $IMAGE_NAME /bin/bash -c " \
        export QT_XCB_GL_INTEGRATION=none && \
        cd /mowbot_legacy_gui && \
        /bin/python3 -m app.main \
    "
