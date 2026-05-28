#!/usr/bin/env bash
set -euo pipefail

jq -c '. | {
  title: .name,
  description: .description,
  url: .html_url,
  tags: ((.topics + (if .language != null then [.language] else [] end)) | join(","))
}'
