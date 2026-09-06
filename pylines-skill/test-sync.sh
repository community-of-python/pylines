#!/usr/bin/env bash
# Self-check for sync.sh: clone -> TTL hit -> forced refetch -> index quality. Needs network.
set -eu
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
export PYLINES_CACHE_DIR="$TMP"

check() { echo "$2" | grep -q "$1" || { echo "FAIL: expected /$1/, got: $2"; exit 1; }; }
absent() { echo "$2" | grep -q "$1" && { echo "FAIL: unexpected /$1/ in $3"; exit 1; }; return 0; }

check "^cloned "      "$(bash "$HERE/sync.sh")"
check "^cache fresh"  "$(bash "$HERE/sync.sh")"
check "^updated "     "$(PYLINES_TTL_MIN=0 bash "$HERE/sync.sh")"
check "^# "           "$(head -1 "$TMP/pylines/code-style.md")"

index="$(cat "$TMP/index.md")"
check "## solid.md"                          "$index"
check "Принцип единой ответственности"       "$index"
absent "Плохо:"                              "$index" index.md   # a comment inside a fenced block
absent "L1     Гайд по SOLID.*L1     "       "$index" index.md   # no duplicate file sections

echo OK
