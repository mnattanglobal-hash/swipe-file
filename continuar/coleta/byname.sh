#!/bin/zsh
# byname.sh <slug> <nome> [scrolls] [session] [country]
SLUG="$1"; Q="${2// /%20}"; N="${3:-10}"; SESS="${4:-s1}"; C="${5:-BR}"
U="https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=${C}&q=${Q}&search_type=page&media_type=all"
"$(dirname "$0")/harvest.sh" "$SLUG" "$U" "$N" "$SESS"
