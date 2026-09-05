#!/usr/bin/env bash
# Self-check for sync.sh: clone -> TTL hit -> forced refetch. Needs network.
set -eu
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
export PYLINES_CACHE_DIR="$TMP"

check() { echo "$2" | grep -q "$1" || { echo "FAIL: expected /$1/, got: $2"; exit 1; }; }

check "^cloned "      "$(bash "$HERE/sync.sh")"
check "^cache fresh"  "$(bash "$HERE/sync.sh")"
check "^updated "     "$(PYLINES_TTL_MIN=0 bash "$HERE/sync.sh")"
check "^# "           "$(head -1 "$TMP/pylines/code-style.md")"

echo OK
