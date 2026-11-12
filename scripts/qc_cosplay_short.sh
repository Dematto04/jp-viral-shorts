#!/bin/bash
set -e
cd "$(dirname "$0")/.."
V="output/Never_Do_This_Cosplay_Japan_Short.mp4"
REPORT="output/QC_REPORT_COSPLAY_SHORT.txt"

{
  echo "=== FFPROBE STREAM & FORMAT ==="
  ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,sample_rate,channels -show_entries format=duration,size,bit_rate -of default=noprint_wrappers=1 "$V"
  echo ""
  echo "=== BLACKDETECT (d=0.10) ==="
  BLK=$(ffmpeg -hide_banner -i "$V" -vf "blackdetect=d=0.10:pix_th=0.10" -an -f null - 2>&1 | grep "black_start" || true)
  if [ -z "$BLK" ]; then
    echo "Zero unwanted black gaps (>=0.10s)"
  else
    echo "$BLK"
  fi
  echo ""
  echo "=== FREEZEDETECT (d=0.40, zero static stills check) ==="
  FRZ=$(ffmpeg -hide_banner -i "$V" -vf "freezedetect=n=-60dB:d=0.40" -an -f null - 2>&1 | grep "freeze_start" || true)
  if [ -z "$FRZ" ]; then
    echo "100% Real-Motion Verified (Zero frozen/static frames >=0.40s)"
  else
    echo "$FRZ"
  fi
  echo ""
  echo "=== EBUR128 INTEGRATED LOUDNESS ==="
  ffmpeg -hide_banner -i "$V" -af ebur128=framelog=verbose -f null - 2>&1 | tail -n 14
} > "$REPORT"

cat "$REPORT"
