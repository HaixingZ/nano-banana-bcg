---
name: nano-banana-bcg
description: "Generate professional BCG-style presentation slides (PPT style) as high-resolution images (PNG) using Google Gemini 3.1 Flash Image. Features green color scheme, consulting layout, and simplified Chinese text. Default resolution 4K. Invoke when user needs professional slides for reports."
metadata:
  emoji: 🍌
  requires:
    bins:
      - uv
    env:
      - GEMINI_API_KEY
  primaryEnv: GEMINI_API_KEY
---


# Nano Banana BCG Style Generator

## Overview

Generate professional, BCG-style presentation slides (images) directly using the Google Gemini API with the `gemini-3.1-flash-image-preview` model.
This skill is pre-configured to produce:
- **Consulting Style**: Clean, minimalist, corporate aesthetics with the BCG green palette.
- **Presentation Ready**: 16:9 aspect ratio, 4K resolution.
- **Format**: High-quality PNG images.

## Usage

### Generate a BCG-style Slide

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "A slide showing the strategic growth pillars for 2025: Market Expansion, Digital Transformation, and Operational Efficiency" \
  --filename growth_strategy.png
```

## Resolution

- Default is `4K` (Ultra High resolution).

## System Prompt

The skill uses a custom system prompt located in `assets/SYSTEM_TEMPLATE` to enforce the BCG design guidelines and PPT layout.

## Setup

Ensure you have your Google Gemini API key set:
1. Get an API key from [Google AI Studio](https://aistudio.google.com/).
2. Set it in your environment or `.env` file:
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```
