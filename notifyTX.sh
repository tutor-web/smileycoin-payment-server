#!/bin/bash

echo "Notifying transaction..."
tokenHeaders=$(curl -I http://127.0.0.1:8000/getToken)
token=$(grep -oP '(?<=csrftoken=).*?(?=;)' <<< "$tokenHeaders")
echo "Got csrf token: $token"
curl -d "$1" --header "X-CSRFToken:$token" --cookie "csrftoken=$token" http://127.0.0.1:8000/postTX

