# Browser CDP Skill

Connect coding agents to a local Chromium-based browser through the Chrome DevTools Protocol (CDP).

## Installation

```bash
npx skills add dlimkin/agent-skills --skill browser-cdp
```

## What this skill does

- Starts an isolated Chromium browser with a local CDP endpoint
- Lists, opens, activates, navigates, inspects, screenshots, and closes tabs
- Uses Node's built-in `fetch` and `WebSocket` without Playwright or Puppeteer
- Supports headless and visible modes and multiple Chromium browser binaries
