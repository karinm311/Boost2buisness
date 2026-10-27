#!/usr/bin/env bash
# Lighthouse: 5 mobile runs (median) + 1 desktop run, then a summary with pass/fail.
#
# usage:  bash tools/lighthouse.sh http://127.0.0.1:8765/ [runs=5] [outdir=lh]
#
# - Test the Netlify build (site/dist) served by tools/serve.py, not the artifact.
# - Scores are noisy, and the first cold run is often lower, so judge by the MEDIAN.
# - Pass bar: Performance, Accessibility, Best Practices and SEO all >= 95,
#   and mobile LCP <= 2.0 s.
set -uo pipefail
URL="${1:?usage: bash tools/lighthouse.sh <url> [runs] [outdir]}"
RUNS="${2:-5}"
OUT="${3:-lh}"
mkdir -p "$OUT"

# Lighthouse needs a Chrome binary. Use Playwright's Chromium when CHROME_PATH isn't set.
if [ -z "${CHROME_PATH:-}" ]; then
  CHROME_PATH="$(python3 -c 'from playwright.sync_api import sync_playwright as s; p=s().start(); print(p.chromium.executable_path); p.stop()' 2>/dev/null)"
  export CHROME_PATH
fi
[ -x "$CHROME_PATH" ] || { echo "Chrome not found. Set CHROME_PATH=/path/to/chrome"; exit 2; }

LH=(npx -y lighthouse@12.2.1)
FLAGS=(--quiet --output=json --only-categories=performance,accessibility,best-practices,seo
       "--chrome-flags=--headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage")

rm -f "$OUT"/m*.json "$OUT"/d*.json
for i in $(seq 1 "$RUNS"); do
  echo "mobile run $i/$RUNS…"
  "${LH[@]}" "$URL" "${FLAGS[@]}" --output-path="$OUT/m$i.json" >/dev/null 2>&1 || echo "  run $i failed"
done
echo "desktop run…"
"${LH[@]}" "$URL" "${FLAGS[@]}" --preset=desktop --output-path="$OUT/d1.json" >/dev/null 2>&1 || echo "  desktop run failed"

python3 "$(dirname "$0")/lh_summary.py" "$OUT"
