#!/usr/bin/env node

import { writeFile } from 'node:fs/promises';

const usage = `Usage:
  node browser-cdp.mjs <browser-url> version
  node browser-cdp.mjs <browser-url> list
  node browser-cdp.mjs <browser-url> open <url>
  node browser-cdp.mjs <browser-url> activate <target-id>
  node browser-cdp.mjs <browser-url> navigate <target-id> <url>
  node browser-cdp.mjs <browser-url> eval <target-id> <expression>
  node browser-cdp.mjs <browser-url> text <target-id>
  node browser-cdp.mjs <browser-url> screenshot <target-id> <output.png>
  node browser-cdp.mjs <browser-url> close <target-id>`;

const [browserUrlArgument, command, ...commandArguments] = process.argv.slice(2);

if (!browserUrlArgument || !command) {
  console.error(usage);
  process.exit(2);
}

if (typeof fetch !== 'function' || typeof WebSocket !== 'function') {
  throw new Error('This helper requires Node.js with built-in fetch and WebSocket.');
}

const browserUrl = new URL(browserUrlArgument);
const loopbackHosts = new Set(['127.0.0.1', 'localhost', '[::1]']);

if (browserUrl.protocol !== 'http:' || !loopbackHosts.has(browserUrl.hostname)) {
  throw new Error('Refusing a non-local CDP endpoint; use an http://127.0.0.1:<port> URL.');
}

async function request(path, options = {}) {
  const response = await fetch(new URL(path, browserUrl.origin), options);

  if (!response.ok) {
    throw new Error(`${options.method ?? 'GET'} ${path} failed with HTTP ${response.status}`);
  }

  const text = await response.text();
  if (!text) return null;

  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

async function pageTarget(targetId) {
  const targets = await request('/json/list');
  const target = targets.find((candidate) => candidate.id === targetId && candidate.type === 'page');

  if (!target) {
    throw new Error(`No page target found for id ${targetId}`);
  }

  if (!target.webSocketDebuggerUrl) {
    throw new Error(`Target ${targetId} does not expose a WebSocket endpoint`);
  }

  return target;
}

class CdpClient {
  static async connect(webSocketUrl) {
    const socket = new WebSocket(webSocketUrl);

    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error('CDP WebSocket connection timed out')), 5000);
      socket.addEventListener(
        'open',
        () => {
          clearTimeout(timeout);
          resolve();
        },
        { once: true },
      );
      socket.addEventListener(
        'error',
        () => {
          clearTimeout(timeout);
          reject(new Error('CDP WebSocket connection failed'));
        },
        { once: true },
      );
    });

    return new CdpClient(socket);
  }

  constructor(socket) {
    this.socket = socket;
    this.nextId = 1;
    this.pending = new Map();

    socket.addEventListener('message', (event) => {
      const message = JSON.parse(String(event.data));
      if (typeof message.id !== 'number') return;

      const pending = this.pending.get(message.id);
      if (!pending) return;

      this.pending.delete(message.id);
      clearTimeout(pending.timeout);

      if (message.error) {
        pending.reject(new Error(message.error.message));
      } else {
        pending.resolve(message.result ?? {});
      }
    });

    socket.addEventListener('close', () => {
      for (const pending of this.pending.values()) {
        clearTimeout(pending.timeout);
        pending.reject(new Error('CDP WebSocket closed before the command completed'));
      }
      this.pending.clear();
    });
  }

  send(method, params = {}) {
    const id = this.nextId++;

    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`CDP command timed out: ${method}`));
      }, 15000);

      this.pending.set(id, { resolve, reject, timeout });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }

  close() {
    this.socket.close();
  }
}

async function withTarget(targetId, action) {
  const target = await pageTarget(targetId);
  const client = await CdpClient.connect(target.webSocketDebuggerUrl);

  try {
    return await action(client);
  } finally {
    client.close();
  }
}

async function evaluate(client, expression) {
  const result = await client.send('Runtime.evaluate', {
    expression,
    awaitPromise: true,
    returnByValue: true,
  });

  if (result.exceptionDetails) {
    const exception = result.exceptionDetails.exception;
    throw new Error(exception?.description ?? result.exceptionDetails.text ?? 'Evaluation failed');
  }

  return result.result?.value ?? result.result?.unserializableValue ?? null;
}

async function waitUntilReady(client) {
  const deadline = Date.now() + 15000;

  while (Date.now() < deadline) {
    try {
      const readyState = await evaluate(client, 'document.readyState');
      if (readyState === 'complete' || readyState === 'interactive') return readyState;
    } catch {
      // The old execution context can disappear while navigation commits.
    }

    await new Promise((resolve) => setTimeout(resolve, 100));
  }

  throw new Error('Page did not become ready within 15 seconds');
}

async function run() {
  switch (command) {
    case 'version': {
      const metadata = await request('/json/version');
      const client = await CdpClient.connect(metadata.webSocketDebuggerUrl);
      try {
        const version = await client.send('Browser.getVersion');
        return { connected: true, ...version };
      } finally {
        client.close();
      }
    }

    case 'list': {
      const targets = await request('/json/list');
      return targets.map(({ id, type, title, url }) => ({ id, type, title, url }));
    }

    case 'open': {
      const [url] = commandArguments;
      if (!url) throw new Error('open requires a URL');
      const target = await request(`/json/new?${encodeURIComponent(url)}`, { method: 'PUT' });
      return { id: target.id, type: target.type, title: target.title, url: target.url };
    }

    case 'activate': {
      const [targetId] = commandArguments;
      if (!targetId) throw new Error('activate requires a target id');
      return { targetId, result: await request(`/json/activate/${encodeURIComponent(targetId)}`) };
    }

    case 'navigate': {
      const [targetId, url] = commandArguments;
      if (!targetId || !url) throw new Error('navigate requires a target id and URL');
      return withTarget(targetId, async (client) => {
        await client.send('Page.enable');
        const navigation = await client.send('Page.navigate', { url });
        if (navigation.errorText) throw new Error(navigation.errorText);
        const readyState = await waitUntilReady(client);
        return { targetId, url, readyState };
      });
    }

    case 'eval': {
      const [targetId, expression] = commandArguments;
      if (!targetId || !expression) throw new Error('eval requires a target id and expression');
      return withTarget(targetId, (client) => evaluate(client, expression));
    }

    case 'text': {
      const [targetId] = commandArguments;
      if (!targetId) throw new Error('text requires a target id');
      return withTarget(targetId, (client) => evaluate(client, "document.body?.innerText ?? ''"));
    }

    case 'screenshot': {
      const [targetId, outputPath] = commandArguments;
      if (!targetId || !outputPath) throw new Error('screenshot requires a target id and output path');
      return withTarget(targetId, async (client) => {
        await client.send('Page.enable');
        const { data } = await client.send('Page.captureScreenshot', {
          format: 'png',
          fromSurface: true,
          captureBeyondViewport: false,
        });
        await writeFile(outputPath, Buffer.from(data, 'base64'));
        return { targetId, outputPath };
      });
    }

    case 'close': {
      const [targetId] = commandArguments;
      if (!targetId) throw new Error('close requires a target id');
      return { targetId, result: await request(`/json/close/${encodeURIComponent(targetId)}`) };
    }

    default:
      throw new Error(`Unknown command: ${command}\n\n${usage}`);
  }
}

try {
  console.log(JSON.stringify(await run(), null, 2));
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
}
