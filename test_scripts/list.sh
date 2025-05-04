#!/bin/bash

work_dir=$(dirname $(realpath $0))

token=$($work_dir/login.sh admin)

curl -s -H "Authorization: Bearer $token" http://localhost:8001/calls | jq
