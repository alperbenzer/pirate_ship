#!/bin/bash

podman run -d \
  --env-file=.env \
  -p 8001:8001 \
  -v $(pwd)/users.db:/app/users.db \
  --name pirate-ui pirate-ui

