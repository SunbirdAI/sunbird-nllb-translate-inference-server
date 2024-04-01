#!/usr/bin/env bash

set -e

# https://www.runpod.io/console/serverless/user/endpoint/vr2cmcpprdmqcq
# The following URLs are available:
#     - https://api.runpod.ai/v2/vr2cmcpprdmqcq/runsync
#     - https://api.runpod.ai/v2/vr2cmcpprdmqcq/run
#     - https://api.runpod.ai/v2/vr2cmcpprdmqcq/health

ENDPOINT=vr2cmcpprdmqcq
RUNPOD_ID=cq3nt9bgf093fo

# echo $RUNPOD_API_KEY

# curl -X 'POST' \
#   "https://api.runpod.ai/v2/${ENDPOINT}/runsync" \
#   -H "accept: application/json" \
#   -H  "authorization: ${RUNPOD_API_KEY}" \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "input": {"prompt": ""}
# }'

http --json GET "https://api.runpod.ai/v2/${ENDPOINT}/health" \
    "Authorization: ${RUNPOD_API_KEY}" \
    "Content-Type: application/json"


http --json POST "https://api.runpod.ai/v2/${ENDPOINT}/runsync" \
    "Authorization: ${RUNPOD_API_KEY}" \
    "Content-Type: application/json" \
    input:='{"source_language": "eng", "target_language": "lug", "text": "Hello, how are you?"}'


http --json POST "https://api.runpod.ai/v2/${ENDPOINT}/runsync" \
    "Authorization: ${RUNPOD_API_KEY}" \
    "Content-Type: application/json" \
    input:='{"source_language": "lug", "target_language": "eng", "text": "Bantu mannyo ga mpisi, gasseka kungulu, nga munda mulimu bussi."}'