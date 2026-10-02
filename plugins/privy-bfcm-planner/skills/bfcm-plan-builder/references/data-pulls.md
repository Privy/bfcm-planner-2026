# Data Pulls: Shopify and Privy

Goal: answer as many planning questions as possible from data, so the interview only covers judgment calls and unknowns. Match on capability, not tool name: connector versions differ. If a tool can't answer something, mark it "Ask in interview."

Keep everything aggregate. Pull counts, sums, percentiles, and top-N lists, not customer-level records in the chat.

**Read only.** Every pull here is a read. Never call Shopify or Privy tools that create, update, or delete anything, and never pull individual customer records: aggregates and counts only. If counts for different filters come back identical, the filter was ignored; don't use them. If a pull fails for lack of permission, skip it and tell the merchant what's missing.

**Timeouts.** If a call times out, retry once with a lighter request: drop comparison periods, ask for fewer rows, or split a long date range. If the retry also fails, skip that pull, tell the merchant what you couldn't read and what it would have added, and carry on. Don't retry the same failing request more than twice.

## Which source for store data

- **Shopify merchants:** use the Shopify connector for all store data (SH1-SH14). It carries customer history, inventory, and discount settings that Privy doesn't.
- **Other platforms (BigCommerce, Wix, Weebly):** there is no connector in the directory, so use Privy's synced order data instead (PV10-PV11). Ask in the interview for what Privy can't supply: inventory on best-sellers, active discount settings, and first-time vs returning split.
- **Shopify merchant without the Shopify connector:** offer to connect it. If they decline, fall back to PV10-PV11 and say so in `basis`.
- Set `meta.platform` from PV1 (`connected_integrations`) and `meta.currency` from the currency codes Privy returns.


**Shopify first when it's connected.** The Shopify connector's analytics tool (`run-analytics-query`, ShopifyQL) returns last year's whole BFCM window in one query, with gross sales, discounts, net sales, and totals as separate figures, plus top products, new vs. returning customers, inventory, and traffic, none of which Privy has. Privy's synced store totals (PV10, one call per day, tax included) are the fallback for stores that aren't on Shopify or haven't connected it. Tested against a seeded Shopify development store on Sep 30, 2026.
## Shopify

| # | Need | How to get it | Used for |
|---|---|---|---|
| SH1 | Shop basics: name, domain, timezone, currency, markets/ship-to countries | Shop info query | Header, send times, suppression of unshippable regions |
| SH2 | Trailing GMV run rate | ShopifyQL (`run-analytics-query`): `FROM sales SHOW orders, gross_sales, net_sales, total_sales, average_order_value SINCE -90d UNTIL today`; multiply by about four for a yearly run rate | GMV band, context for the snapshot |
| SH3 | Last year's BFCM window: revenue, orders, AOV | ShopifyQL: `FROM sales SHOW orders, gross_sales, discounts, net_sales, total_sales, average_order_value SINCE 2025-11-20 UNTIL 2025-12-05`. Gross, discounts, net, and total come back separately, so say which one a figure is | Baselines, discount depth last year |
| SH4 | New vs returning customers in that window | ShopifyQL: `FROM sales SHOW customers, new_customers, returning_customers, returning_customer_rate SINCE 2025-11-20 UNTIL 2025-12-05`. A customer can count as both new and returning in one window, so never add the two; use `returning_customer_rate` | Offer and nurture emphasis |
| SH5 | Top 10 products in that window, plus current inventory | ShopifyQL: `FROM sales SHOW net_sales, gross_sales, orders GROUP BY product_title SINCE 2025-11-20 UNTIL 2025-12-05 ORDER BY net_sales DESC LIMIT 10`, then `FROM inventory SHOW ending_inventory_units, inventory_units_sold, sell_through_rate GROUP BY product_title SINCE -30d UNTIL today ORDER BY inventory_units_sold DESC LIMIT 10`. Compare units on hand with last BFCM's orders for each hero product. Ignore obvious test products (a single high-priced item with one or two orders) | Hero products, sellout risk, fallback picks |
| SH6 | Discount codes used last BFCM and overall discount rate | ShopifyQL: `FROM sales SHOW orders, discounts, gross_sales GROUP BY discount_code SINCE 2025-11-20 UNTIL 2025-12-05 ORDER BY orders DESC LIMIT 10`. A blank code means automatic or manually applied discounts. Discount rate = discounts / gross sales | Offer depth history, stacking audit |
| SH7 | Currently active discounts, with combination settings | Admin GraphQL (`graphql_query`, after `validate_graphql_codeblocks`): `discountNodes(first: 20, query: "status:active")` with `... on DiscountCodeBasic` / `DiscountAutomaticBasic` / `DiscountCodeBxgy` / `DiscountAutomaticBxgy` / free-shipping types, reading `title`, `startsAt`, `endsAt`, `codes`, and `combinesWith { orderDiscounts productDiscounts shippingDiscounts }` | Stacking audit: a welcome or popup code that combines with order discounts can stack on the sale |
| SH8 | Customer spend and order-count tiers | **Use Privy, not Shopify.** Shopify's `customersCount(query:)` silently ignores `orders_count` and `total_spent` filters and returns every customer, which looks plausible and is wrong. Privy segments on lifetime spend (all-time) and order count return real counts (PV6). Use Shopify's average order value (SH2) to help set the spend threshold | VIP threshold, segment sizing |
| SH9 | Lapsed customers | Privy segments (last order date), PV6 | Win-back segment sizes |
| SH10 | Collections | Admin GraphQL `collectionsCount { count }`, then `search_collections` for names (gift, sale, top categories) | Category segments (S16), Gift Shoppers (S14), Discount Shoppers (S18) |
| SH11 | Subscriptions | Admin GraphQL `sellingPlanGroups(first: 1) { nodes { id name } }`; none means no subscription program | Active Subscribers segment (S15) relevance |
| SH12 | Current AOV (last 90 days) | Same query as SH2 (`average_order_value`) | Tier thresholds, free-shipping threshold |
| SH13 | Daily revenue by order date, Nov 20 - Dec 5 2025 | ShopifyQL: `FROM sales SHOW orders, gross_sales, discounts, net_sales, total_sales TIMESERIES day SINCE 2025-11-20 UNTIL 2025-12-05`: one query for the whole chart (Privy needs one summary call per day) | Review chart |
| SH14 | Repeat rate of last BFCM's new customers: share who ordered again since | First-order date in the 2025 window, later orders | Review finding, nurture step |
| SH15 | Traffic and conversion in last year's window | ShopifyQL: `FROM sessions SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout, conversion_rate SINCE 2025-11-20 UNTIL 2025-12-05`. Privy has no traffic data. Stores seeded through the API have no sessions; treat near-zero sessions alongside real orders as missing data | Popup reach, conversion context |

Derivations:
- **GMV band:** SH2 annualized. Under $5M = lean band; $5M-$20M = scaled band (see best-practices section 14).
- **VIP threshold:** the 90th-95th percentile of lifetime spend from SH8, rounded to a clean number, or "3+ orders" if that yields a more sensible size. Report the resulting count.
- **High-spend cutoff:** about the 75th-80th percentile of lifetime spend.
- **Tier thresholds:** first tier about 1.2-1.5x current AOV (SH12).
- **Baseline (not a target):** report SH3 revenue for core and extension as last year's actuals. Do not compute a target or forecast from it.
- **Sellout risk:** for each hero SKU, current inventory vs last BFCM units sold. Flag anything under 1.5x last year's units.

## Privy

**Telemetry:** leave optional telemetry fields (`agent_thinking`, `user_intent`, `user_frustration`) out of every call. If one is required, a few neutral words about the call's purpose.

Endpoints below are from the Privy connector (all read-only GET). Call `describe` before the first use of each: the contracts carry the semantics that matter here. Each session reads the signed-in merchant's own account.

| # | Need | Endpoint and how | Used for |
|---|---|---|---|
| PV0 | Privy tenure, profile, and sending recency | `/v1/reports/summary` for last year's window: any attributed revenue or sends means `returning`. `/v1/reports/campaigns` (newest first) for `privy_last_send`; earliest send for `privy_first_send`. A summary for the last 90 days with zero sends and signups means the merchant went quiet (churned and returned) | Profile, and whether a warm-up is required |
| PV1 | Platform, integrations, live display types, flow triggers in use | `/v1/account/setup` (`summary.connected_integrations`, `live_display_types`, `flow_triggers_in_use`) | `meta.platform`, loyalty app (e.g. a points program means F13 applies), scope |
| PV2 | **Total mailable and total textable** | Two calls to `GET /v1/contacts` with `per_page=10`: one with `email_consent=subscribed` (total mailable), one with `sms_consent=subscribed` (total textable). Read **only** `pagination.total_count`. The response also returns 10 full contact records: never show, quote, or keep them. Never use the unfiltered `total_count` (it counts every contact, whatever their consent), and never count `single_opt_in` or `pending` as textable. If a call fails (for example `409 contacts_not_ready`), retry once, then say the count couldn't be read | The first two figures in Today at Privy, list size in the snapshot, audience sizing |
| PV3 | Displays and signup rates | `/v1/reports/displays` (last 90 days); `/v1/reports/summary` `signups`, `signup_rate` (signups divided by popup views, not visitors: say "of popup views lead to a signup") | Display tasks, Today stats |
| PV4 | Flows: status **and results** | `/v1/reports/flows` (last 90 days) is the primary pull: one call returns every flow with `status`, channels, current enrollment, and sent, order rate, attributed revenue, unsubscribes, and SMS failures. Judge flows by what's `active`; drafts and duplicates are common, and a live flow can carry a test name. For a returning merchant with nothing active, run it for last Oct-Dec to see what used to work, and look for rebuilt drafts ready to turn on. `/v1/flows/{id}` for delays and coupon sync on the flows the plan changes. An empty result means no flows in the current system | F01-F15 status, flow tasks driven by results (a flow converting well below its peers gets fixed first; a channel that converts better, like SMS in a cart flow, gets added where it's missing), "Already set" |
| PV4b | Settings for every flow the plan changes | `/v1/flows/{id}` for each flow a task will touch: its steps, delays, discounts, filters, and who it skips. Quote these in the task; never assume them | Flow tasks |
| PV5 | Last year's campaigns | `/v1/reports/campaigns` with `period=custom`, Nov 20 - Dec 5 last year, both pages; `type=flows` separately if needed. **Drop rows with `sent` = 0** (drafts and tests). Row stats are dated by event (`event_date` basis) and never total to the summary | Findings (VIP vs full list, fatigue across sends, SMS results), send timing |
| PV6 | Segments and sizes | `/v1/segments` (`mailable_count`, `textable_count`, `refreshed_at`). Match existing segments to S01-S20 before planning builds | "Already set" vs build tasks |
| PV7 | Engagement health | Prebuilt "Unengaged Contacts" count (check `refreshed_at`); `/v1/reports/summary` `unsubscribe_rate`; campaign `bounce_rate` and `spam_reports` on recent sends | Deliverability tasks |
| PV8 | Existing early-access list, tag, or segment | `/v1/segments` names; display and flow titles | S02, F03 |
| PV9 | Attributed revenue for last year's sale window | `/v1/reports/summary`, custom window. Report `attributed_revenue` total plus `by_channel` (email, sms) and `by_type` (campaign, flow) as two separate splits, basis `send_date`. If the window is before the account's reporting boundary, the splits come back null and revenue is dated when attributed: show the total only, basis `attribution_date` | Review channel line |
| PV10 | Store totals, any platform | `/v1/reports/summary` `totals_context` (`total_orders`, `total_revenue`, order-date basis, tax included). Daily chart: one call per day. Null before the reporting boundary | Review stats and daily chart when Shopify isn't available |
| PV11 | Discount codes and top products, any platform | `/v1/reports/top_products`; `/v1/coupons`. `/v1/orders` only if unavoidable: rows carry names, emails, and addresses, and busy windows run to thousands of rows | Offer history, stacking audit |
| PV12 | Privy capability questions | `search_help_docs`, then `read_help_article` for the full article (Privy connector, help.privy.com). Use it before any task that depends on a feature, above all on non-Shopify platforms | Skips with reasons instead of research tasks; `basis.data` note |

**Platform limits confirmed in the help center** (re-check with PV12 if in doubt, since features change): on BigCommerce there is no Back In Stock flow and no browse abandonment (no browse tracking), checkout abandonment works on the standard Optimized One-Page Checkout only, and unique coupon codes aren't supported in campaigns (use one master code created in BigCommerce). Back In Stock needs Shopify or Shopify Plus.

**Accounts are messy.** The same store can have more than one Privy account (use the one tied to the connected store, with API access). Some accounts return no splits or store totals even for recent periods, so handle nulls everywhere, not only before July 1, 2026. A returning merchant can come back with no live displays or active flows (`/v1/account/setup` shows empty lists): plan the rebuild, not updates.

**Zero popup views isn't proof a popup is broken.** Check store traffic first (Shopify sessions, SH15). If sessions are near zero too, treat it as an unknown to verify, not a finding.

**Read the numbers critically.** Flag anomalies instead of reporting them: rates over 100%, SMS where a large share fail to deliver (Privy registers its sending numbers with carriers, so registration usually isn't the merchant's fix; look first at the list, meaning invalid, landline, or disconnected numbers and numbers that fail repeatedly, and at message content carriers may filter, and if failures stay high, suggest asking Privy support to check delivery), SMS click rates far above email (link previews and bots inflate them), or a day of zero display signups mid-sale (displays switched off or broken). Label segment counts with their refresh date, and label comparisons that straddle the reporting boundary as approximate.

## Where each pull appears in the plan

| Pull | On the page |
|---|---|
| SH3, SH4, SH13, SH14 (or PV10) | Starting point: Last BFCM stats, daily chart, first-time buyer return rate |
| PV9 | Starting point: Privy revenue line (send date, or attribution date before the boundary) |
| PV2, PV3, PV4, PV7 | Starting point: Today |
| SH5, SH6, SH7, SH8, SH10, PV3, PV4, PV6 | Task details (thresholds, sizes, codes, displays) and task evidence |
| PV5 | Send calendar timing |
| Everything pulled, with date ranges | What this plan is based on |

## Mapping evidence to checklist status

- Flow exists and is on, and its offer/delays already match BFCM guidance: **Ready**.
- Flow exists but uses an evergreen code, long delays, or a discount that would stack: **Needs update**.
- Flow does not exist: **Missing** (priority from checklist).
- Segment exists with sensible rules: **Ready**; exists but stale thresholds: **Needs update**; absent: **Missing**.
- Popup offer conflicts with the BFCM offer or would stack: **Needs update**.
- Anything neither tool can see (checkout load test, UTMs, legal review, DMARC status, shipping cutoffs): **Unknown** until the interview answers it.

## Shopify vs Privy revenue

Shopify records revenue on the order date. Privy attributes revenue to the send date of the message that drove it. Window totals roughly agree; daily figures don't. Use Shopify for anything by day (SH13, live monitoring vs last year) and Privy for channel totals (PV9) and per-send results. Never put Privy daily revenue next to Shopify daily revenue, and label any share that mixes them as approximate. See `plan-data-spec.md` section 4.

## When the merchant is new to Privy

If PV0 shows no Privy activity during last year's BFCM, don't treat the missing PV5 history as a gap to fill with benchmarks. Follow `new-to-privy.md`: Shopify supplies the sales baseline, Privy data since joining supplies the rates (if 30+ days), and the merchant can optionally share results from before Privy.

## When data is partial or missing

- Label partial pulls in the snapshot ("based on the first 10,000 orders").
- If Shopify is not connected, ask the merchant for: last BFCM revenue/orders/AOV, annual GMV, AOV, customer count, and top products.
- If Privy is not connected, ask for: email and SMS list sizes, which flows are on, and current popup offers.
- Never fill a gap with a benchmark silently. Say "Using the industry benchmark of X because we don't have your number."
