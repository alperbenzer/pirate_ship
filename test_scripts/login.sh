#!/bin/bash

username=$1

if [ ! -z $1 ]
then

read -s -p "password : " password

curl -s -X POST -F "username=$username" -F "password=$password" http://localhost:8001/login | jq .access_token | sed 's/\"//g'

else
echo "provide username"
fi