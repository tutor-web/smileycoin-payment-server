#!/bin/bash

tokenHeaders=$(curl -I http://127.0.0.1:5000/getToken)
token=$(grep -oP '(?<=csrftoken=).*?(?=;)' <<< "$tokenHeaders")
echo "Got csrf token: $token"

curl -d "$1" --header "X-CSRFToken:$token" --cookie "csrftoken=$token" http://127.0.0.1:5000/postTX

