#!/bin/sh
set -eu
: "${HANZO_API_KEY:?Set HANZO_API_KEY}"
curl --fail-with-body --silent --show-error --max-time 30  "${HANZO_BASE_URL:-https://api.hanzo.ai/v1}/worlds"  -H "Authorization: Bearer $HANZO_API_KEY" -H 'Content-Type: application/json'  -d '{"model":"sekai-1-alpha","domain":"simulation"}'
