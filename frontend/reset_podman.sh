#!/bin/bash

podman stop pirate-ui
podman rm pirate-ui
podman build -t pirate-ui .

podman run -d \
  --name pirate-ui \
  --network pirate-net \
  -p 8003:80 \
  pirate-ui

podman ps
