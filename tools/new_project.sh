#!/usr/bin/env bash
# Create a new case project from the template.
# Usage: tools/new_project.sh "suspect-name-city"
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLUG="${1:?usage: tools/new_project.sh <slug>}"
DIR="$ROOT/projects/$(date +%Y-%m)-$SLUG"
[ -e "$DIR" ] && { echo "exists: $DIR"; exit 1; }
mkdir -p "$ROOT/projects"; cp -r "$ROOT/templates/project" "$DIR"
echo "created $DIR"
echo "next: fill research/sources.md, timeline.md, people.md, assets.csv  (docs/04_production_workflow.md §②)"
