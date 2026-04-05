# Flexbe webhooks — detailed reference

## How it works

Flexbe sends a POST request to your configured URL immediately after an event.
Delivery is real-time; no polling required.

Configure webhook URLs in **Settings → API → Event handler URLs**.

---

## Request format

| Property               | Value                                        |
|------------------------|----------------------------------------------|
| HTTP method            | POST                                         |
| Content-Type           | `application/x-www-form-urlencoded`          |
| Encoding               | UTF-8                                        |

---

## Root fields

```
$_REQUEST['event']  →  "lead" | "pay"
$_REQUEST['site']   →  array — site info
$_REQUEST['data']   →  array — lead/payment data
```

### `site` object

| Field    | Type    | Description                            |
|----------|---------|----------------------------------------|
| `id`     | integer | Flexbe account ID                      |
| `sub_id` | integer | Landing page (page group) ID           |
| `domain` | string  | Site domain, e.g. `yourdomain.com`     |
| `name`   | string  | Landing page name                      |

---

## `data` object — full field list

Identical structure in both `lead` and `pay` events, except where noted.

### Top-level fields

| Field       | Type      | Description                         |
|-------------|-----------|-------------------------------------|
| `id`        | integer   | Unique lead ID                      |
| `num`       | integer   | Human-readable lead number          |
| `time`      | timestamp | Unix timestamp of lead creation     |
| `status`    | object    | `{code, name}` — lead status        |
| `client`    | object    | Client contact info                 |
| `note`      | string    | Lead notes                          |
| `form_name` | string    | Name of the lead form               |
| `form_data` | object    | All form field values (arbitrary)   |
| `page`      | object    | Page the lead was submitted from    |
| `utm`       | object    | UTM parameters                      |
| `pay`       | object    | Invoice / payment info              |

### `status` object

| Field  | Type    | Description              |
|--------|---------|--------------------------|
| `code` | integer | Status code (0–11)       |
| `name` | string  | Status label             |

Codes: `0` New · `1` Processed · `2` Fulfilled · `10` Cancelled · `11` Deleted

### `client` object

| Field   | Type   | Description          |
|---------|--------|----------------------|
| `name`  | string | Full name            |
| `phone` | string | Phone number         |
| `email` | string | Email address        |

### `page` object

| Field  | Type   | Description         |
|--------|--------|---------------------|
| `url`  | string | Full page URL       |
| `name` | string | Page name           |

### `utm` object

| Field          | Description                              |
|----------------|------------------------------------------|
| `utm_source`   | Traffic source / ad system               |
| `utm_campaign` | Campaign name                            |
| `utm_medium`   | Channel type (cpc, email, organic…)      |
| `utm_term`     | Keyword                                  |
| `utm_content`  | Ad variant                               |
| `url`          | Full URL including all UTM parameters    |

### `pay` object

| Field         | Type      | `lead` event       | `pay` event        |
|---------------|-----------|--------------------|--------------------|
| `id`          | integer   | Invoice ID         | same               |
| `summ`        | float     | Amount due         | same               |
| `status`      | object    | Usually `0` Pending| `2` Paid or `3` Error |
| `time_create` | timestamp | Invoice created at | same               |
| `time_done`   | timestamp | Usually empty      | Filled on success  |
| `desc`        | string    | Buyer comment      | same               |
| `pay_link`    | string    | Payment page link  | same               |
| `test`        | boolean   | **Present** — sandbox flag | **Absent** |

Payment status codes: `0` Pending · `1` In process · `2` Paid · `3` Error

> **`pay.test`** — present only in `lead` events. `true` means the payment was processed
> through the gateway's test/sandbox server. No real money was charged.
> Always check this flag before running business logic (activating access, shipping, etc.).

---

## Event differences at a glance

| Aspect               | `lead` event                        | `pay` event                          |
|----------------------|-------------------------------------|--------------------------------------|
| Trigger              | Form submitted → lead created       | Gateway sends payment notification   |
| `pay.status.code`    | Typically `0` (Pending)             | `2` (Paid) or `3` (Error)            |
| `pay.time_done`      | Usually null                        | Filled when code = `2`               |
| `pay.test` field     | Present (`true` or `false`)         | **Not present**                      |

---

## Typical event sequences

**Successful purchase:**
```
→  lead event   (pay.status.code = 0  "Pending payment")
→  pay  event   (pay.status.code = 2  "Paid",  time_done filled)
```

**Failed payment:**
```
→  lead event   (pay.status.code = 0  "Pending payment")
→  pay  event   (pay.status.code = 3  "Payment error")
```

**Lead without payment:**
```
→  lead event   (pay object is empty or absent)
```

---

## Full raw request example (print_r)

```
[event] => lead
[site] => Array
    (
        [id]     => 174911
        [sub_id] => 180023
        [domain] => yourdomain.com
        [name]   => Landing page
    )
[data] => Array
    (
        [id]        => 1414
        [num]       => 414
        [time]      => 1444215670
        [status]    => Array ( [code] => 0  [name] => New )
        [client]    => Array
            (
                [name]  => Ivan Ivanov
                [phone] => +79001234567
                [email] => ivan@example.com
            )
        [note]      =>
        [form_name] => Main form
        [form_data] => Array ( ... )
        [page]      => Array ( [url] => https://yourdomain.com/ [name] => Home )
        [utm]       => Array
            (
                [utm_source]   => google
                [utm_campaign] => summer
                [utm_medium]   => cpc
                [utm_term]     =>
                [utm_content]  =>
                [url]          => https://yourdomain.com/?utm_source=google
            )
        [pay]       => Array
            (
                [id]          => 555
                [summ]        => 1500
                [status]      => Array ( [code] => 0 [name] => Pending payment )
                [time_create] => 1444215670
                [time_done]   =>
                [desc]        => Order payment
                [test]        =>
            )
    )
```

---

## Handler examples

### PHP (full)

```php
<?php
// webhook_handler.php
$event = $_REQUEST['event'] ?? '';
$site  = $_REQUEST['site']  ?? [];
$data  = $_REQUEST['data']  ?? [];

switch ($event) {

    case 'lead':
        $lead_id = $data['id'];
        $num     = $data['num'];
        $client  = $data['client'];
        $utm     = $data['utm'];

        // Save to database
        // $db->insert('leads', [...]);

        // Email notification
        // mail('manager@company.com', "New lead #{$num}", ...);

        // Payment check
        if (!empty($data['pay']['id'])) {

            // Skip test payments
            if (!empty($data['pay']['test'])) {
                error_log("Test payment for lead #{$num} — skipped");
                break;
            }

            // Real pending payment — send invoice email etc.
        }
        break;

    case 'pay':
        $code    = $data['pay']['status']['code'];
        $lead_id = $data['id'];

        if ($code === 2) {
            $paid_at = date('Y-m-d H:i:s', $data['pay']['time_done']);
            // Grant access, ship product, etc.
            // activateService($lead_id, $paid_at);
        }

        if ($code === 3) {
            // Notify customer about failed payment
            // sendPaymentErrorEmail($data['client']['email']);
        }
        break;

    default:
        error_log("Unknown Flexbe event: {$event}");
}

http_response_code(200);
echo 'ok';
```

### Node.js / Express (full)

```javascript
const express = require('express');
const app = express();
app.use(express.urlencoded({ extended: true }));

app.post('/flexbe/webhook', (req, res) => {
    const { event, site, data } = req.body;

    if (event === 'lead') {
        const { id, num, client, utm, pay } = data;
        console.log(`New lead #${num}: ${client.name} (${client.phone})`);

        if (utm?.utm_source) {
            console.log(`Source: ${utm.utm_source} / ${utm.utm_campaign}`);
        }

        if (pay?.test) {
            console.log('Sandbox payment — ignoring');
        }
    }

    if (event === 'pay') {
        const code = data.pay.status.code;

        if (code === 2) {
            console.log(`Lead #${data.id} paid at`, new Date(data.pay.time_done * 1000));
            // activateService(data.id);
        }
        if (code === 3) {
            console.log(`Lead #${data.id} — payment error`);
            // notifyPaymentError(data.client.email);
        }
    }

    res.status(200).send('ok');
});

app.listen(3000, () => console.log('Flexbe webhook listener running on :3000'));
```

---

## Security recommendations

Flexbe documentation does not describe a request signature (HMAC) mechanism.
Recommended mitigations:

1. **Use HTTPS** for your webhook URL.
2. **Validate `site.domain` or `site.id`** in the request body to confirm the source matches your site.
3. **Restrict by IP** if Flexbe's server IPs are known and stable (check with support).
4. **Always check `pay.test`** before executing irreversible business actions.
