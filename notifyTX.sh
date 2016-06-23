#!/bin/bash

echo "Notifying transaction..."
tokenHeaders=$(curl -I http://smileyservice.herokuapp.com/getToken)
token=$(grep -oP '(?<=csrftoken=).*?(?=;)' <<< "$tokenHeaders")
echo "Got csrf token: $token"

curl -d "$1" --header "X-CSRFToken:$token" --cookie "csrftoken=$token" http://smileyservice.herokuapp.com/postTX

