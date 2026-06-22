---
name: personal-video-clones
description: "Create short personal clone videos of Jose/JT for sending to people: script, voice/avatar workflow, safety/consent checks, and platform-specific packaging."
version: 1.0.0
metadata:
  hermes:
    tags: [video, avatar, voice-clone, personal-brand, messaging, cloning]
    related_skills: [media-content-workflows, humanizer]
---

# Personal Video Clones

Use this when JT asks to generate, plan, script, or send a short personalized video where a digital version of him addresses someone directly.

## Core Safety Rule

Only create clones of **JT himself** or people who have explicitly provided consent. Do not help impersonate third parties, fake evidence, bypass platform rules, or present AI-generated media as real. For outbound videos, include a light disclosure when appropriate: “te mandé este video con mi avatar/AI clone” or visual text like “AI avatar de Jose”.

## Intake Questions

Ask only what is needed. If the user is moving fast, infer sensible defaults and proceed with a draft.

1. Recipient: who is this for?
2. Goal: sell, invite, follow up, apologize, thank, explain, update, pitch, reminder?
3. Tone: warm, casual, professional, funny, direct, bilingual/spanglish?
4. Length: default 20–45 seconds for WhatsApp/Telegram; 60–90 seconds for demos.
5. Medium: WhatsApp, Telegram, email, LinkedIn, Instagram, website embed?
6. Source assets: does JT already have a trained avatar/voice in HeyGen, ElevenLabs, Captions, Tavus, Synthesia, etc.?

## Default Output Package

Return a compact package:

- **Video title/internal label**
- **Recipient-specific script** (spoken)
- **On-screen caption text** (optional)
- **Generation prompt/instructions** for the chosen tool
- **Send message** to accompany the video
- **Disclosure line** if needed

## Script Formula: 20–45 sec Personalized Clone

Use this structure:

1. Hook with recipient name/context: “Hey [Name], soy Jose…”
2. Personal reason: “te mando esto porque…”
3. One clear message/offer/request.
4. Low-friction next step: “si te late, respóndeme con…”
5. Human close: “abrazo / gracias / te debo una chela / hablamos”.

Keep it natural. Avoid corporate AI language: “excited to”, “leverage”, “game-changer”, “synergy”, “revolutionary”.

## Spanish Template

```text
Hey [Nombre], soy Jose. Te mando este videíto rápido porque [contexto personal].

La idea es simple: [mensaje principal en una frase]. Creo que te puede servir porque [beneficio específico para esa persona].

Si te late, respóndeme con [acción fácil: “sí”, “mándame info”, “qué día”, etc.] y lo vemos rápido.

Abrazo.
```

## English Template

```text
Hey [Name], Jose here. Quick personal video because [specific context].

The short version is: [main point]. I thought of you because [specific reason/benefit].

If this sounds useful, just reply with [easy next step] and I’ll send you the details.

Talk soon.
```

## Spanglish Template

```text
Hey [Name], soy Jose. Quick one — te mando esto porque [contexto].

The idea is pretty simple: [main point]. Creo que puede hacer sentido para ti porque [specific reason].

Si te late, just reply “[keyword]” y te mando el siguiente paso.

Abrazo.
```

## Tool Workflows

### A) Fastest No-Code Workflow

Use when user wants something today from phone/browser:

1. Script in Hermes.
2. Generate voice/avatar in HeyGen/Captions/Tavus/Synthesia if trained.
3. Add captions in CapCut/Captions.
4. Export vertical 9:16 MP4 under 45 seconds.
5. Send via WhatsApp/Telegram with a short companion text.

### B) Voice Clone + B-roll Workflow

Use when a talking head avatar is unnecessary:

1. Generate voice with authorized JT voice clone (ElevenLabs/MiniMax/etc.).
2. Combine with photos, screen recordings, or branded slides.
3. Add subtitles.
4. Export MP4.

### C) Browser-Only Work Laptop Friendly Workflow

Because JT’s work computer is locked down, prefer browser/mobile tools and avoid requiring local CLI:

- HeyGen, Captions, Tavus, Synthesia, ElevenLabs web UI, CapCut web/mobile.
- If Hermes needs to produce files, create scripts/prompts/text assets and send them back through Telegram.

## Quality Checklist

Before finalizing:

- Script sounds like JT, not a corporate bot.
- One recipient, one purpose, one CTA.
- Under 45 seconds unless user asked longer.
- Personal detail included.
- No fake claim that JT personally recorded it live.
- If avatar/AI clone could be misleading, include disclosure.
- Message to send with video is included.

## Recommended Asset Capture for JT Clone

If the user asks how to train the clone:

- Record 2–5 minutes selfie video in good light, quiet room.
- Look at camera, normal pace, neutral background.
- Include Spanish and English samples if bilingual clone is needed.
- Capture multiple tones: warm invite, professional pitch, casual follow-up.
- Use only platforms where JT controls consent and usage rights.

Suggested recording prompt:

```text
Soy Jose Torres. Estoy grabando esta muestra para crear mi propio avatar/voz digital con mi consentimiento. Quiero que suene natural, cercano y útil. A veces voy a usarlo para mandar mensajes personalizados, explicar ideas rápido, dar seguimiento a proyectos y comunicarme mejor cuando no pueda grabar un video manualmente.

En español quiero sonar casual, directo y humano. In English, I want to sound warm, clear, and concise. Not salesy, not robotic — just like me sending a quick personal update.
```

## Final Response Pattern

When JT requests a clone video, respond with:

```text
Listo. Te dejo el paquete:

**Script:**
...

**Caption:**
...

**Prompt/instrucciones para [tool]:**
...

**Mensaje para mandar junto al video:**
...
```
