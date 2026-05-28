# Transcription Runtime Notes — Divine Pharma Cron

Session learning from processing `Ep. 8 - Heme Drugs` (52:06 MP3, ~48 MB):

## What worked

- Full-episode Whisper on CPU with `base` timed out at 10 minutes and did not emit a text file.
- Full-episode Whisper on CPU with `tiny` was still too slow for a cron turn and timed out before completion.
- Splitting the MP3 into ~8-minute chunks and transcribing each chunk with `tiny` completed successfully. Seven chunks produced a combined transcript (~47k chars).

## Recommended fallback command pattern

```bash
mkdir -p /tmp/divine_pharma/chunks /tmp/divine_pharma/chunk_txt
ffmpeg -hide_banner -loglevel error -i /tmp/divine_pharma/episode.mp3 \
  -f segment -segment_time 480 -c copy /tmp/divine_pharma/chunks/chunk%03d.mp3

for f in /tmp/divine_pharma/chunks/chunk*.mp3; do
  base=$(basename "$f" .mp3)
  if [ ! -s "/tmp/divine_pharma/chunk_txt/$base.txt" ]; then
    whisper "$f" --model tiny --language English \
      --output_dir /tmp/divine_pharma/chunk_txt --output_format txt --verbose False
  fi
done

python3 - <<'PY'
from pathlib import Path
files = sorted(Path('/tmp/divine_pharma/chunk_txt').glob('chunk*.txt'))
text = '\n\n'.join(p.read_text(errors='ignore') for p in files)
Path('/tmp/divine_pharma/transcript.txt').write_text(text)
print(f'combined {len(files)} chunks, {len(text)} chars')
PY
```

## Pitfalls

- Avoid embedding Python heredocs inside heavily nested single-quoted `bash -lc '...'` strings; quotes can be stripped and produce syntax like `Path(/tmp/...)`. Prefer writing a short helper script with `write_file`, or run `python3 - <<'PY'` as the top-level command string.
- `whisper --verbose False` still prints progress bars; run it in a background process and poll/wait if needed.
- Store the noisy raw transcript separately in `Transcripts/YYYY-MM-DD-...-Transcript.md` and keep the daily note cleaned/corrected for study use.
- Tiny-model transcripts may phonetically mangle medical terms (`heme pharmacology`, `vWF`, `GpIb`, `GpIIb/IIIa`, `P2Y12`, etc.); correct obvious terms in the study note instead of copying raw transcript verbatim.
