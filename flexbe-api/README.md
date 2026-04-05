# flexbe-api

> Claude skill — full reference for the [Flexbe](https://flexbe.com) landing page platform API and webhook system.

Gives Claude deep knowledge of the Flexbe REST API so it can write integration code, explain methods, handle webhook events, and debug API responses without hallucinating field names or inventing methods.

---

## What it covers

- **REST API** — authentication, `checkConnection`, `getLeads` (with all filter params and returned fields), `changeLead`
- **Webhooks** — `lead` and `pay` events, complete field-by-field payload reference, event sequencing, `pay.test` flag
- **Error codes** and rate limits
- **Code examples** in PHP, Node.js, and cURL

---

## Installation

```bash
npx skills add dlimkin/agent-skills --skill flexbe-api
```

---

## Usage

Once installed, Claude automatically consults the skill when you ask anything Flexbe API-related. No special syntax needed.

**Example prompts that trigger the skill:**

```
Write a PHP webhook handler for Flexbe that saves new leads to MySQL
and sends a Telegram message when a payment is confirmed.
```

```
How do I filter getLeads to return only paid leads from the last 7 days?
```

```
What's the difference between the lead and pay webhook events?
What fields are present in one but not the other?
```

```
Generate a Node.js Express endpoint that receives Flexbe webhooks,
ignores test payments, and calls my /activate API on successful payment.
```

```
Restore all deleted Flexbe leads using changeLead via the API.
```

---

## Skill structure

```
flexbe-api/
├── SKILL.md              — quick reference, all methods, code snippets
└── references/
    └── webhooks.md       — complete webhook payload reference,
                            full PHP & Node.js handler examples,
                            event sequences, security notes
```

`SKILL.md` is always loaded when the skill triggers.
`references/webhooks.md` is loaded on demand when webhook details are needed.

---

## Source

Based on the official Flexbe API documentation:
https://help.flexbe.com/api-documentation/

API support: dev@flexbe.com
