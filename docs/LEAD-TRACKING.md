# Lead tracking: dispatch.texassolutions.co

Updated 13 October 2026. GA4 property: `G-ZKMGJ4L8NG` (loads only on texassolutions.co hosts).

## Events the site sends

| Event | Fires when | Is it a lead? |
|---|---|---|
| `lead_form_submit` | Inquiry form saved successfully by Web3Forms (success response only) | **Yes** (confirmed inquiry) |
| `callback_request` | Callback form saved successfully | **Yes** (confirmed callback request) |
| `lead_form_error` | Form could not be sent (network or rejected) | No |
| `click_call` | A `tel:` link is tapped | No, interest only |
| `click_text` | An `sms:` link is tapped | No, interest only |
| `click_whatsapp` | A WhatsApp link is tapped | No, interest only (WhatsApp opening is not a lead) |
| `cta_click` (`cta` = `talk` / `first_load`) | "Talk to a Dispatcher" or "Start Your First Load Free" clicked | No, interest only |
| `tool_start`, `tool_calculate` | A calculator is used (the fee calculator is `estimate`) | No |

Event parameters: `form_id`, `equipment`, `trucks`, `mc_status`, `contact_method`, `sms_consent` (yes/no), `link_location`, `page_path`, and `campaign_source/medium/campaign` from UTM tags. **No names, phone numbers, emails or messages are sent to GA4.**

Each inquiry email also carries the landing page, referrer and UTM values (`attribution_*` fields), the page it was sent from, the intent (`talk_to_dispatcher` or `first_load_free`) and a submission ID.

## One-time GA4 setup (owner)

1. Admin → Events: mark `lead_form_submit` and `callback_request` as **key events**. Do not mark the click events as key events.
2. Admin → Data streams → Enhanced measurement → Form interactions: **turn off** to avoid a second, generic `form_submit` count.
3. Admin → Custom definitions: add event-scoped dimensions `form_id`, `equipment`, `link_location`, `cta`, `tool_name`.
4. Reports → Explore → Free form, saved as "Dispatch leads":
   - Rows: Country, Landing page, Session source / medium
   - Values: Active users, Event count filtered to `lead_form_submit`, `callback_request`, `click_call`, `click_text`, `click_whatsapp`
   - Filter: Country = United States
   - Second tab: Page path contains `-dispatch` or `/truck-dispatch/` (service and state pages), Views
5. Test: GA4 DebugView, or add `?debug_mode=1` and confirm one `lead_form_submit` per successful send.

## Qualified carriers and signed clients

GA4 cannot know who qualified or signed. Keep `docs/lead-log-template.csv` (or a Google Sheet with the same columns) updated from the inquiry emails, using the submission ID to match each email. Monthly report = GA4 numbers above plus counts of `qualified = yes` and `signed = yes` from the log.

## Test results (13 Oct 2026)

- Local, forced network failure: error shown, typed details kept, button re-enabled, `lead_form_error` only, no false success.
- Local, empty form: browser validation, no request sent.
- Local, mocked success: confirmation shown, single `lead_form_submit`.
- Live: one labelled test inquiry ("TEST INQUIRY - website check") submitted from /contact.html; Web3Forms returned success. Delivery to dispatch@texassolutions.co must be confirmed in the inbox. GA was in debug mode, so the test was not counted as a lead.
- Click events: `click_call`, `click_text`, `click_whatsapp`, `cta_click` each fire once per click.
