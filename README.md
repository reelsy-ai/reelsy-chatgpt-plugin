# Reelsy for ChatGPT

Create and edit Reelsy videos directly from ChatGPT.

## Capabilities

- Generate Reelsy videos from natural-language requests and show ready results on Reelsy Canvas.
- Open Hosted OpenCut for timeline editing only after the user explicitly requests or confirms editing.
- Add captions, hosted fonts, music, stickers, dynamic visual elements, transitions, and foundational edits.
- Connect the user's Reelsy account through OAuth without asking for an API key.

## Production connection

This plugin connects only to the production MCP provided by the Reelsy main service:

```text
https://reelsy.ai/api/codex/mcp
```

Installation, authorization, and tool verification do not create paid Jobs or deduct credits. Before any paid generation, the Agent must show the expected credit cost and wait for the user's explicit confirmation.

## Skills

```text
skills/reelsy-video-production
skills/reelsy-video-editing
skills/reelsy-ecommerce-product-ad
skills/reelsy-ugc-creator-video
skills/reelsy-motion-clone
skills/reelsy-narrative-remix
```

`reelsy-video-production` and `reelsy-video-editing` provide the two foundational capabilities. The four domain Skills select the appropriate production or editing workflow without bypassing the main-service MCP, OAuth ownership, or credit boundaries.

## Get started

Copy the following prompt into a task in ChatGPT Desktop:

```text
/goal Read reelsy.ai/chatgpt to install the Reelsy plugin, connect my Reelsy account, and start a new video creation task for me.
```

See [Reelsy ChatGPT setup](https://reelsy.ai/chatgpt) for installation and recovery instructions.

## Publishing boundary

This repository contains the public Reelsy Plugin package. Never commit local MCP addresses, API keys, OAuth tokens, user project data, or development environment configuration.
