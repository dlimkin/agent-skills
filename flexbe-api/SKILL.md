---
name: flexbe-api
description: >
  Full reference for the Flexbe landing page platform REST API and webhook system.
  Use this skill whenever the user asks about Flexbe API integration, reading or changing leads,
  handling webhooks, processing payments, working with UTM data, or writing any code that
  connects to Flexbe (PHP, Node.js, cURL). Trigger on phrases like "Flexbe API", "лиды Flexbe",
  "webhook Flexbe", "интеграция Flexbe", "getLeads", "changeLead", "flexbe webhook",
  "обработать лид", "платёж Flexbe".
---

# Flexbe API skill

Covers the complete Flexbe REST API: authentication, methods (`getLeads`, `changeLead`),
webhook events (`lead`, `pay`), error codes, rate limits, and code examples in PHP, Node.js,
and cURL.

## Quick reference

| What                | Value                                              |
|---------------------|----------------------------------------------------|
| Base URL            | `http://{your_domain}/mod/api/`                    |
| Auth param          | `?api_key={key}`                                   |
| Response format     | JSON, UTF-8, data in `data` object                 |
| Rate limit          | 100 requests/min                                   |
| Max leads/request   | 1 000 (use `start` + `count` for pagination)       |
| Webhook method      | POST to your script URL                            |
| Webhook events      | `lead` (new lead), `pay` (payment notification)    |
| Support             | dev@flexbe.com                                     |

## Error codes

| Code | Meaning                  |
|------|--------------------------|
| `0`  | Invalid `api_key`        |
| `1`  | Rate limit exceeded      |
| `2`  | Nonexistent method       |

Error response shape: `{ "error": { "code": 0, "msg": "Invalid api_key" } }`

## Lead status codes

| Code | Name      |
|------|-----------|
| `0`  | New       |
| `1`  | Processed |
| `2`  | Fulfilled |
| `10` | Cancelled |
| `11` | Deleted   |

## Payment status codes

| Code | Name               |
|------|--------------------|
| `0`  | Pending payment    |
| `1`  | Payment in process |
| `2`  | Paid               |
| `3`  | Payment error      |

---

## Methods

Method is passed as `&method=methodName` in the query string.

### `checkConnection`

```
GET /mod/api/?api_key={key}&method=checkConnection
→ {"status":1}
```

### `getLeads`

Returns leads sorted newest-first.

**Filter params:**

| Param          | Type      | Default | Description                              |
|----------------|-----------|---------|------------------------------------------|
| `status`       | integer   | —       | Filter by lead status code               |
| `date_from`    | timestamp | —       | Created at ≥ this Unix timestamp         |
| `date_to`      | timestamp | —       | Created at ≤ this Unix timestamp         |
| `client_phone` | string    | —       | Exact phone match                        |
| `client_email` | string    | —       | Exact email match                        |
| `start`        | integer   | 0       | Pagination offset                        |
| `count`        | integer   | 25      | Page size (max 1 000)                    |

**Lead object fields:** `id`, `num`, `time`, `status{code,name}`, `client{name,phone,email}`,
`note`, `form_name`, `form_data`, `page{url,name}`, `utm{utm_source,utm_campaign,utm_medium,utm_term,utm_content,url}`,
`pay{id,summ,status{code,name},time_create,time_done,desc,pay_link}`

### `changeLead`

**Required:** `id` (lead identifier)

**Optional:** `status`, `client{name,phone,email}`, `note`,
`pay{summ, status (0-3), desc}`

---

## Code snippets

### cURL — get leads by email
```bash
curl 'http://yourdomain.com/mod/api/?api_key=XXXXX&method=getLeads&client_email=user@example.com'
```

### PHP — get leads for the last month
```php
require('flexbe_api.class.php');
$flexbe = new flexbeAPI('http://yourdomain.com/mod/api/', 'YOUR_API_KEY');

$leads = $flexbe->getLeads([
    'date_from' => strtotime('-1 month'),
    'date_to'   => strtotime('today UTC'),
]);
```

### PHP — restore deleted lead
```php
if ($lead['status'] == 11) {
    $flexbe->changeLead($lead['id'], ['status' => 10]);
}
```

### Node.js — get new leads
```javascript
const request = require('request');
const flexbeAPI = {
    url: 'http://yourdomain.com/mod/api/',
    api_key: 'YOUR_API_KEY',
    query(method, params, cb) {
        params.api_key = this.api_key;
        params.method  = method;
        request.post({ uri: this.url, form: params },
            (err, res, body) => { try { cb(JSON.parse(body)); } catch(e) { console.error(e); } });
    }
};

flexbeAPI.query('getLeads', { status: 0 }, result => {
    console.log(result.data.leads);
});
```

---

## Webhooks — overview

Flexbe sends a **POST** request to your script URL on each event.
No polling needed. Configure URLs in **Settings → API**.

**Request body fields:**

| Field   | Description                                   |
|---------|-----------------------------------------------|
| `event` | Event type: `"lead"` or `"pay"`               |
| `site`  | `{id, sub_id, domain, name}`                  |
| `data`  | Full lead object (same shape as `getLeads`)   |

> For the complete webhook field reference, event-by-event differences,
> PHP/Node.js handler examples, and security notes — read
> **`references/webhooks.md`**.

### Minimal PHP handler
```php
<?php
$event = $_REQUEST['event'];
$data  = $_REQUEST['data'];

if ($event === 'lead') {
    // new lead — $data has id, num, client, utm, pay, pay.test flag, etc.
}
if ($event === 'pay') {
    // payment update — $data['pay']['status']['code'] is 2 (paid) or 3 (error)
}

http_response_code(200);
echo 'ok';
```

### Key webhook rules
- Always respond **HTTP 200** to acknowledge receipt.
- Check `$data['pay']['test']` in `lead` events — it flags sandbox payments (no real money).
- The `test` flag is **absent** in `pay` events.
- Typical flow: `lead` (status 0 Pending) → `pay` (status 2 Paid **or** 3 Error).
