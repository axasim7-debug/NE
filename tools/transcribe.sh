#!/usr/bin/env bash
# Transcribe every file in footage/raw → footage/transcripts/<id>.srt using Whisper.
# Usage: tools/transcribe.sh projects/<slug> [model=small]
# Install once: pip install openai-whisper   (needs ffmpeg)
set -euo pipefail
P="${1:?project dir}"; M="${2:-small}"
mkdir -p "$P/footage/transcripts"
for f in "$P"/footage/raw/*.{mp4,mov,mkv,webm,wav,mp3,m4a}; do
  [ -e "$f" ] || continue
  b=$(basename "${f%.*}")
  [ -e "$P/footage/transcripts/$b.srt" ] && { echo "skip $b"; continue; }
  echo "→ $b"
  whisper "$f" --model "$M" --language en --output_format srt --output_dir "$P/footage/transcripts"
done
