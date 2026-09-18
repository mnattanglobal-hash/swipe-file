#!/bin/zsh
# deepdive.sh <slug> <page_id> [scrolls] [session] [country]
SLUG="$1"; PID="$2"; N="${3:-12}"; SESS="${4:-s1}"; C="${5:-BR}"
U="https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=${C}&view_all_page_id=${PID}&search_type=page&media_type=all"
"$(dirname "$0")/harvest.sh" "$SLUG" "$U" "$N" "$SESS"
