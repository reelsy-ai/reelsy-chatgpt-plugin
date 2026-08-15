# Reelsy for ChatGPT

Create and edit Reelsy videos directly from ChatGPT.

## Capabilities

- Generate Reelsy videos from natural-language requests and show ready results on Reelsy Canvas.
- Open Hosted OpenCut for timeline editing only after the user explicitly requests or confirms editing.
- Generate a vocal song, rewrite a user-authorized source song, or create instrumental music after explicit 12-credit confirmation.
- Keep source analysis, lyric rewriting, timed captions, audio replacement, and final video editing under Codex control; Reelsy only performs the paid music generation step.
- Add captions, hosted fonts, stickers, dynamic visual elements, transitions, and foundational edits.
- Connect the user's Reelsy account through OAuth without asking for an API key.

## Production connection

This plugin connects only to the production MCP provided by the Reelsy main service:

```text
https://reelsy.ai/api/codex/mcp
```

Installation, authorization, and tool verification do not create paid Jobs or deduct credits. OAuth makes the owner-scoped video and music tools available to ChatGPT; it does not itself start a generation. Before any paid generation, the Agent must show the expected credit cost and wait for the user's explicit confirmation.

## Skills

```text
skills/reelsy-video-production
skills/reelsy-video-editing
skills/reelsy-song-rewrite
skills/reelsy-ecommerce-product-ad
skills/reelsy-ugc-creator-video
skills/reelsy-motion-clone
skills/reelsy-narrative-remix
```

`reelsy-video-production` and `reelsy-video-editing` provide the two foundational capabilities. `reelsy-song-rewrite` coordinates Codex-local source analysis, approved lyric rewriting, Reelsy music generation, captions, and final editing. The remaining domain Skills select the appropriate production or editing workflow without bypassing the main-service MCP, OAuth ownership, or credit boundaries.

## Get started

### Add from GitHub

In ChatGPT Desktop, open **Plugins**, choose **Add**, and select **Add plugin marketplace**. Use the repository below, keep the Git ref as `main`, and leave **Sparse paths** empty:

```text
https://github.com/reelsy-ai/reelsy-chatgpt-plugin
```

The repository includes a Marketplace manifest at `.agents/plugins/marketplace.json`. It points to the root Plugin package, so do not enter `plugins/codex` or another sparse path.

If your host only exposes the single-plugin installer, use **Add plugin** with the same repository URL and leave the ref/path fields at their defaults.

After installation, copy the following prompt into a new task in ChatGPT Desktop:

```text
/goal Read reelsy.ai/chatgpt to install the Reelsy plugin, connect my Reelsy account, and start a new video creation task for me.
```

See [Reelsy ChatGPT setup](https://reelsy.ai/chatgpt) for installation and recovery instructions.

## Publishing boundary

This repository contains the public Reelsy Plugin package. Never commit local MCP addresses, API keys, OAuth tokens, user project data, or development environment configuration.
