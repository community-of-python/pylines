#!/usr/bin/env bash
# Refresh pylines guides cache from GitHub. Safe offline (keeps old cache).
set -u
REPO="https://github.com/community-of-python/pylines"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CACHE_ROOT="${PYLINES_CACHE_DIR:-$SKILL_DIR/cache}"
DIR="$CACHE_ROOT/pylines"
STAMP="$CACHE_ROOT/.fetch-stamp"
TTL_MIN="${PYLINES_TTL_MIN:-60}"
unset HTTPS_PROXY HTTP_PROXY https_proxy http_proxy  # public host: claude-fwd proxy is Anthropic-only

emit() { echo "$1"; echo "guides: $DIR"; }

if [ ! -d "$DIR/.git" ]; then
  mkdir -p "$CACHE_ROOT"
  git clone --depth 1 -q "$REPO" "$DIR" || { echo "pylines: no cache and clone failed"; exit 1; }
  touch "$STAMP"
  emit "cloned ($(git -C "$DIR" rev-parse --short HEAD))"
  exit 0
fi

if [ "$TTL_MIN" -gt 0 ] && [ -n "$(find "$STAMP" -mmin "-$TTL_MIN" 2>/dev/null)" ]; then
  emit "cache fresh (<${TTL_MIN}m, $(git -C "$DIR" rev-parse --short HEAD))"
  exit 0
fi

if git -C "$DIR" fetch --depth 1 -q origin main && git -C "$DIR" reset --hard -q origin/main; then
  touch "$STAMP"
  emit "updated ($(git -C "$DIR" rev-parse --short HEAD))"
else
  emit "fetch failed (offline?) — using cached copy"
fi
