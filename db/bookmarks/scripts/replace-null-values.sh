#!/usr/bin/env bash
set -euo pipefail

jq -c 'walk(if . == null then "" else . end)'
