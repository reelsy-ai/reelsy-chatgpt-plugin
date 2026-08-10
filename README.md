# Reelsy for ChatGPT

通过 ChatGPT 使用 Reelsy 的视频生成与编辑能力。

## 能力范围

- 通过自然语言生成 Reelsy 视频，并将可用结果展示在 Reelsy Canvas。
- 在用户明确要求或确认后，进入 Hosted OpenCut 进行时间线编辑。
- 支持字幕、托管字体、音乐、贴纸、动态视觉元素、转场和基础剪辑。
- 通过 OAuth 连接 Reelsy 账号，不需要用户创建或粘贴 API Key。

## 生产连接

本插件只连接 Reelsy 主站提供的生产 MCP：

```text
https://reelsy.ai/api/codex/mcp
```

安装、授权和工具验证不会创建付费 Job，也不会扣减积分。任何付费生成都必须先展示预计积分并等待用户明确确认。

## Skills

```text
skills/reelsy-video-production
skills/reelsy-video-editing
skills/reelsy-ecommerce-product-ad
skills/reelsy-ugc-creator-video
skills/reelsy-motion-clone
skills/reelsy-narrative-remix
```

两个基础能力是 `reelsy-video-production` 和 `reelsy-video-editing`。其他领域 Skill 负责选择合适的生产或编辑流程，不绕过主站 MCP 的 OAuth、资源归属和积分边界。

## 开始使用

在 ChatGPT Desktop 的任务中复制并发送：

```text
/goal Read reelsy.ai/chatgpt to install the Reelsy plugin, connect my Reelsy account, and start a new video creation task for me.
```

安装说明和恢复规则见 [Reelsy ChatGPT setup](https://reelsy.ai/chatgpt)。

## 发布说明

当前仓库内容面向 Reelsy 的公开 Plugin 发布。请勿将本地 MCP 地址、API Key、OAuth Token、用户项目数据或开发环境配置提交到仓库。
