# Case study: completing a 30-minute live-site `skipped_no_gpu` placeholder on CPU

Session: 2026-07-02 scheduled Divine Pharmacology cron run.

## Scenario

A prior scheduled run had already discovered the latest live-site episode and created in-place placeholder notes:

- Daily note: `/root/Divine-Pharmacology/Daily-Sessions/2026-07-02-DIP-Ep-661-The-Genetics-Sprint-for-Step-2-and-3-Part-1.md`
- Transcript note: `/root/Divine-Pharmacology/Transcripts/2026-07-02-DIP-Ep-661-The-Genetics-Sprint-for-Step-2-and-3-Part-1-Transcript.md`
- Audio: `/root/Divine-Pharmacology/Audio/2026-07-02-DIP-Ep-661-The-Genetics-Sprint-for-Step-2-and-3-Part-1.mp3`
- Placeholder markers: `processing_status: structured_fallback_no_transcript`, `transcription_status: skipped_no_gpu_episode_1810s`, and body text such as `Structured fallback created from episode metadata`.

The episode was not pharmacology-specific but was still a Divine/USMLE high-yield genetics episode, so the correct action was to complete the existing placeholder rather than create a duplicate or return `[SILENT]`.

## CPU transcription result

Command pattern used:

```python
from faster_whisper import WhisperModel
from pathlib import Path

AUDIO = Path('/root/Divine-Pharmacology/Audio/2026-07-02-DIP-Ep-661-The-Genetics-Sprint-for-Step-2-and-3-Part-1.mp3')
RAW = Path('/root/Divine-Pharmacology/Transcripts/2026-07-02-DIP-Ep-661-The-Genetics-Sprint-for-Step-2-and-3-Part-1.txt')
SEG = Path('/root/Divine-Pharmacology/Transcripts/2026-07-02-DIP-Ep-661-The-Genetics-Sprint-for-Step-2-and-3-Part-1-segments.tsv')

model = WhisperModel('base', device='cpu', compute_type='int8')
segments, info = model.transcribe(str(AUDIO), beam_size=5, vad_filter=True)
texts = []
with SEG.open('w', encoding='utf-8') as sf:
    sf.write('start\tend\ttext\n')
    for seg in segments:
        txt = seg.text.strip()
        if txt:
            texts.append(txt)
            sf.write(f'{seg.start:.2f}\t{seg.end:.2f}\t{txt}\n')
RAW.write_text(' '.join(texts).strip(), encoding='utf-8')
```

Observed output:

- Audio size: 25,049,244 bytes
- Episode duration: 1,810.6 seconds (`00:30:10`)
- Model: `faster-whisper base`, `device='cpu'`, `compute_type='int8'`, `vad_filter=True`
- Transcript: 35,757 chars
- Segments: 363
- Elapsed wall time: 567.2 seconds

## Important timing lesson

A 30-minute episode can finish inside a 600-second foreground cron tool timeout, but only narrowly. Do not skip simply because there is no GPU. However, after starting a 30+ minute CPU transcription, avoid extra expensive work before the timeout. If the tool environment allows a longer timeout/background job, prefer it for episodes over ~30 minutes; otherwise, use the 600-second foreground ceiling and be prepared to fall back to `tiny` or chunking only if base CPU actually times out.

## In-place completion steps

1. Reuse the existing audio file instead of downloading again.
2. Write both raw transcript `.txt` and timestamped `segments.tsv`.
3. Replace the transcript placeholder note with frontmatter `transcription_status: completed` plus links to the raw transcript and segments TSV.
4. Replace the original Daily-Sessions placeholder with `processing_status: completed` and `transcription_status: completed`, preserving the original path/date.
5. Ensure the processed log contains both the live hash and canonical URL variants.
6. Verify the two touched notes have no placeholder markers:
   - `Transcription failed`
   - `Content pending transcription`
   - `structured fallback`
   - `To be extracted from transcript`
   - `skipped_no_gpu`
   - `transcription_status: skipped`
   - `processing_status: structured_fallback`

## Content extraction note

Whisper may mangle medical names (`Duchenne`, `Marfan`, `Ehlers-Danlos`, `achondroplasia`, etc.). Use the transcript for structure but normalize obvious medical terminology in the study note. For this case, the note emphasized gene/inheritance/mechanism differentials for CF, sickle cell disease, Duchenne/Becker, Huntington, Fragile X, Marfan, Ehlers-Danlos, osteogenesis imperfecta, and achondroplasia.
