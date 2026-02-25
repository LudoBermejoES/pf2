#!/usr/bin/env bash
# Descarga subtítulos de playlists de YouTube (sin descargar vídeo)
# Uso: ./scripts/download-subtitles.sh

set -e

OUTPUT_DIR="$(dirname "$0")/../subtitulos"
mkdir -p "$OUTPUT_DIR"

PLAYLISTS=(
  "https://www.youtube.com/playlist?list=PLYCDCUfG0xJag_jvYu8sreK4pkA5ogZN5"
  "https://www.youtube.com/playlist?list=PLYCDCUfG0xJb5I-wDIezuDkTfbd8k21Km"
  "https://www.youtube.com/playlist?list=PLYCDCUfG0xJboH84xXJly1J00afbRJMRT"
  "https://www.youtube.com/playlist?list=PLYCDCUfG0xJagSmaiCko8XEe5wD4MXFdL"
  "https://www.youtube.com/playlist?list=PLYCDCUfG0xJY9BZxsauuu9NbUValAblrD"
)

for PLAYLIST in "${PLAYLISTS[@]}"; do
  echo ""
  echo "=========================================="
  echo "Procesando: $PLAYLIST"
  echo "=========================================="

  yt-dlp \
    --skip-download \
    --write-auto-sub \
    --write-sub \
    --sub-lang "es,es-ES,es-419,en" \
    --sub-format "vtt" \
    --convert-subs "srt" \
    --ignore-errors \
    --output "$OUTPUT_DIR/%(playlist_title)s/%(playlist_index)03d - %(title)s.%(ext)s" \
    "$PLAYLIST"
done

echo ""
echo "Subtítulos descargados en: $OUTPUT_DIR"
