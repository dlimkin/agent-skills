---
name: browser-cdp
description: Connect to and inspect a local Chromium-based browser session over CDP.
version: 1.0.0
---

# Browser CDP

Connect an agent to a local Chromium-based browser through the Chrome DevTools
Protocol (CDP), then list, open, inspect, navigate, capture, and close tabs with
terminal capabilities. The supplied helpers use only a Chromium browser, Bash,
and Node's built-in `fetch` and `WebSocket`; Playwright and Puppeteer are not
required.

This skill does not retrofit CDP onto an already-running browser process that was
started without remote debugging. It does not expose the CDP port to the
network, reuse the normal browser profile, or bypass a site login.

## When to Use

- Connect to a Chromium browser and inspect the page.
- Open the local app in a browser and check the rendered UI.
- Read page text or evaluate JavaScript in a browser tab.
- Take a screenshot from a browser.
- Verify that the agent can control a Chromium browser.

## Prerequisites

- Linux with one of these Chromium browsers on `PATH`: `vivaldi`,
  `google-chrome`, `google-chrome-stable`, `chromium`, `chromium-browser`,
  `brave-browser`, or `microsoft-edge`.
- Bash, `curl`, `jq`, `sed`, and Node.js with global `fetch` and
  `WebSocket`.
- A graphical session for `visible` mode. Use `headless` when no display or
  manual interaction is needed.
- Helper directory: `scripts/` in this skill directory.

Check the local prerequisites before starting:

```bash
command -v vivaldi google-chrome google-chrome-stable chromium chromium-browser brave-browser microsoft-edge node curl jq sed
node -e "console.log({fetch: typeof fetch, WebSocket: typeof WebSocket})"
```

## Procedure

1. Check whether the requested browser is already CDP-enabled. Do not assume
   that any running browser process is attachable merely because it exists.

   ```bash
   pgrep -a -f 'chrome|chromium|brave|edge.*remote-debugging' || true
   ss -ltnp | rg ':9222\b' || true
   curl --fail --silent http://127.0.0.1:9222/json/version | jq .
   ```

   If `/json/version` responds, use that browser URL. If it does not, start an
   isolated session in the next step. Never restart or terminate the user's
   normal browser unless they explicitly request it.

2. Start an isolated browser session. Run this helper through the command
   execution capability and keep its returned command session alive:

   ```bash
   scripts/start-browser-cdp.sh headless
   ```

   Use `visible` instead of `headless` when the user needs to interact with the
   browser. The helper accepts a browser binary as a positional argument or via
   `BROWSER_CDP_BIN`, binds CDP to `127.0.0.1`, requests a free port with
   `--remote-debugging-port=0`, creates a fresh `--user-data-dir`, and prints:

   ```text
   BROWSER_CDP_BROWSER_URL=http://127.0.0.1:<port>
   BROWSER_CDP_PROFILE=/tmp/browser-cdp.<suffix>
   BROWSER_CDP_PID=<pid>
   BROWSER_CDP_BIN=<selected-browser>
   ```

   Retain the browser URL and command-session ID. Sending `stop` to the command
   session stops the browser and removes the disposable isolated profile.

3. Verify both the HTTP discovery endpoint and the CDP WebSocket connection:

   ```bash
   browser_cdp_url=http://127.0.0.1:<port>
   browser_cdp_tool=scripts/browser-cdp.mjs
   curl --fail --silent "$browser_cdp_url/json/version" | jq '{Browser, "Protocol-Version", webSocketDebuggerUrl}'
   node "$browser_cdp_tool" "$browser_cdp_url" version
   ```

   Continue only when the helper prints `"connected": true`.

4. List current targets and open the requested URL:

   ```bash
   node "$browser_cdp_tool" "$browser_cdp_url" list
   node "$browser_cdp_tool" "$browser_cdp_url" open 'http://127.0.0.1:5003/'
   ```

   Record the page target `id` returned by `open` or `list`. Never choose an
   extension, service worker, or background target; inspect targets whose `type`
   is `page`.

5. Inspect or manipulate only the target relevant to the user's request:

   ```bash
   browser_target_id='<page-target-id>'
   node "$browser_cdp_tool" "$browser_cdp_url" activate "$browser_target_id"
   node "$browser_cdp_tool" "$browser_cdp_url" eval "$browser_target_id" '({title: document.title, url: location.href, readyState: document.readyState})'
   node "$browser_cdp_tool" "$browser_cdp_url" text "$browser_target_id"
   node "$browser_cdp_tool" "$browser_cdp_url" navigate "$browser_target_id" 'http://127.0.0.1:5003/orders'
   node "$browser_cdp_tool" "$browser_cdp_url" screenshot "$browser_target_id" /tmp/browser-page.png
   ```

   Inspect the generated PNG with the available local-image viewing
   capability. Quote JavaScript expressions and URLs so the shell does not
   interpret them.

6. Close only an agent-created tab when it is no longer needed:

   ```bash
   node "$browser_cdp_tool" "$browser_cdp_url" close "$browser_target_id"
   ```

7. Stop the isolated browser by sending `stop` followed by a newline to the
   still-running launcher command session. Confirm that the launcher reports
   completion and that the CDP URL no longer responds. Do not kill unrelated
   browser processes.

## Pitfalls

- Remote debugging cannot be enabled retroactively on an existing process.
- Chromium 136+ ignores remote-debugging switches for the default data
  directory. A non-default `--user-data-dir` is therefore mandatory and also
  protects the user's real cookies and sessions.
- A CDP endpoint has no application-level authentication and grants broad
  control over its profile. Keep it on `127.0.0.1`; never bind it to `0.0.0.0`
  or forward it over the network without an explicit security design.
- An isolated profile starts logged out. Let the user authenticate in `visible`
  mode if the requested page requires credentials; never copy the normal
  profile or extract its cookies.
- `--remote-debugging-port=0` deliberately chooses a different port each time.
  Read the printed browser URL rather than assuming port 9222.
- Keep the launcher command session alive. On `stop`, interruption, or
  termination, its cleanup trap stops the isolated browser and removes the
  temporary profile after validating its `browser-cdp.??????` path.
- `eval` runs JavaScript in the page's main world. Use read-only expressions
  unless the user requested a page interaction or state change.

## Verification

Run a disposable end-to-end check:

1. Start the launcher in `headless` mode and retain its browser URL.
2. Run `version` and confirm `"connected": true`.
3. Run `open` with a known URL, retain the target ID, and run `eval` with
   `document.title`.
4. Run `screenshot` and verify that the PNG is non-empty and viewable.
5. Send `stop` to the launcher session and verify that requesting
   `/json/version` now fails.

The connection is proven only after the WebSocket command succeeds; an open TCP
port or a successful `/json/version` response alone is not sufficient.

Primary references:

- https://developer.chrome.com/blog/remote-debugging-port
- https://chromedevtools.github.io/devtools-protocol/
- https://chromedevtools.github.io/devtools-protocol/tot/Page/
- https://chromedevtools.github.io/devtools-protocol/tot/Runtime/
