---
name: ascii-media
description: "Use when creating ASCII art or ASCII video: terminal text banners, cowsay/boxes compositions, image-to-ASCII, and colored ASCII MP4/GIF conversions."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ascii, art, video, gif, terminal, media]
    related_skills: []
---

# ASCII Media

## Overview

This umbrella covers ASCII output as a class, from quick terminal art to full colored ASCII video conversions. Preserve the user's requested medium: plain text, ANSI terminal output, image, GIF, or MP4.

## When to Use

- The user asks for ASCII art, banners, cowsay, boxes, or text-mode illustrations.
- The user asks to convert an image to ASCII.
- The user asks to convert video/audio into colored ASCII MP4/GIF.

## Static ASCII Art

Use lightweight terminal tools such as pyfiglet, cowsay, boxes, and image-to-ascii conversion. Keep monospaced formatting intact and avoid Markdown wrapping that damages alignment.

## ASCII Video

For video/audio conversions, extract frames/audio, map visuals into colored ASCII frames, render to MP4/GIF, and verify the media output exists and plays/analyzes correctly.

## Common Pitfalls

1. Losing alignment through proportional fonts or wrapped Markdown.
2. Ignoring terminal width constraints.
3. Producing huge frame dumps instead of a media file for video tasks.
4. Failing to verify generated media.

## Verification Checklist

- [ ] Output medium chosen.
- [ ] Static art alignment checked or media file generated.
- [ ] File existence/size verified for media outputs.
- [ ] Final response preserves formatting or includes media path.
