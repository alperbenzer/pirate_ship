#!/bin/bash

if [ ! -z $2 ]
then

work_dir=$(dirname $(realpath $0))

token=$($work_dir/login.sh admin)

curl -s -X PATCH -H "Authorization: Bearer $token" \
  -F "doc_id=$2" \
  http://localhost:8001/calls/$1/doc | jq

else
echo "usage update_status.sh ID DOC_ID"
fi