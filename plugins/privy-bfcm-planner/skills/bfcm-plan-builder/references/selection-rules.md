# Selection Rules: Which Flows and Segments Make the Plan

The checklists are a menu, not a to-do list. Most merchants need a subset. A plan with 8 flows and 7 segments that all get done beats a plan with 35 items that stall half-built.

Run this in stage 5, before prioritizing. Every item ends up in one of three buckets:

- **Include:** it's in the plan with an action, owner, and due date.
- **Adjust only:** it already exists and just needs a BFCM change (pause, swap code, shorten delay). Include it, because leaving an existing flow untouched is how stacking accidents and off-message sends happen. These are usually quick.
- **Skip:** not in the plan. List it under "Skipped and why" with a one-line reason so the merchant can add it back.

## The test every item must pass

A segment earns a place only if it gets something different: a different message, offer, timing, or exclusion. If it would receive the exact same sends as its parent audience, fold it in.

A flow earns a place if it already exists (then it's Adjust only), or if it's Core, or if its condition below is met **and** there's time and capacity to build it well.

Additional rules:
- **Minimum size:** segments under about 250 contacts rarely justify separate creative. Fold them into a broader segment unless they are a suppression.
- **No net-new optional flows inside 28 days of Black Friday.** Note them for after the window or next year instead. Core flows are the exception.
- **No overlapping segments for the same send.** If the spend/frequency matrix (S07-S10) is used, don't also target Repeat Customers (S13) separately; the matrix covers them. VIPs take precedence over any segment they overlap.

## Flows

| ID | Flow | Tier | Include when |
|---|---|---|---|
| F01 | Welcome Series (Email) | Core | Always (every Privy merchant collects email) |
| F02 | Welcome Series (SMS) | Conditional | SMS is enabled in Privy |
| F03 | BFCM Early Access Signup | Core if early access | The merchant is offering early access (interview B4) |
| F04 | Popup Coupon Reminder | Conditional | A live popup gives a code (PV3) |
| F05 | Abandoned Cart | Core | Always |
| F06 | Browse Abandonment | Optional | Exists, or scaled band with capacity and 29+ days left |
| F07 | Back In Stock | Conditional | A waitlist/back-in-stock feature exists, or hero SKUs have sellout risk |
| F08 | Order Confirmation / Thank You | Adjust only | Privy (not just Shopify) sends a post-purchase message; otherwise fold shipping-cutoff copy into Shopify's notification as an ops item |
| F09 | Post-Purchase Cross-Sell | Optional | Exists, or the catalog has clear complements and capacity allows |
| F10 | Review Request | Adjust only | Exists (action: pause or extend delay) |
| F11 | Replenishment | Conditional | Consumable products with a predictable reorder cycle |
| F12 | Post-BFCM New Customer Nurture | Core | Always (build before the sale, launch after delivery) |
| F13 | VIP Tier Entry | Conditional | A loyalty or VIP program exists |
| F14 | Win-Back | Adjust only | Exists (action: pause or reroute into BFCM sequence) |
| F15 | Birthday / Anniversary | Adjust only | Exists and birthdays are collected |

Typical result: 4-5 Core flows plus 2-5 Adjust-only or Conditional flows.

## Segments

| ID | Segment | Tier | Include when |
|---|---|---|---|
| S01 | VIPs | Core | Always |
| S02 | BFCM Early Access | Core if early access | Early access is offered |
| S03 | Last BFCM New Customers | Conditional | Ran BFCM last year and acquired roughly 250+ new customers in the window |
| S04 | Last BFCM One-Time Buyers | Conditional | Same as S03 and many haven't returned; merge with S03 if the message is the same |
| S05 | Engaged Non-Buyers | Core | Always |
| S06 | New Subscribers 30D | Conditional | An active list-growth push is running (it usually is) |
| S07-S10 | Spend/frequency matrix | Optional | Scaled band, each cell 500+ contacts, and the merchant will send distinct messages to each; otherwise use VIPs + Repeat Customers |
| S11 | Lapsed 90-365D | Core | Always (sizeable in almost every store) |
| S12 | Lapsed 365D+ | Conditional | Sizeable and deliverability is healthy; one send only |
| S13 | Repeat Customers | Conditional | Matrix not used |
| S14 | Gift Shoppers | Conditional | A gift collection or gift cards exist |
| S15 | Active Subscribers | Conditional | A subscription app is in use |
| S16 | Category: [Name] | Conditional | Distinct categories with different hero products; 1-3 segments max, not one per collection |
| S17 | Bought: [Item] | Optional | A hero product with an obvious complement |
| S18 | Discount Shoppers | Conditional | A sale collection exists |
| S19 | Recent Buyers 7D | Core (launch email only) | Always |
| S20 | Unengaged 90D+ | Core (suppression) | Always |

Typical result: 6-8 segments for a lean team, 10-14 for a scaled team.

## Readiness items (R16-R48)

Include by default, except:
- R18 Spin-to-Win: only if one is live.
- R20, R32, R39 (SMS items): only if SMS is enabled.
- R22 New vs Returning targeting: optional for lean teams.
- R34 Checkout load test: for Shopify stores this is test orders with every code and combination, not a load test. Shopify handles capacity.
- R44 Real-time dashboard: lean teams get a daily check routine instead of a dashboard.

## Merchants new to Privy

If the merchant wasn't live on Privy for last year's BFCM, apply the lean scope regardless of GMV band, and use the substitutes in `new-to-privy.md` section 4 for engagement-based segments (S05, S20, engagement tiers). Skip S03/S04 for stores with no BFCM history. Present Missing flows as "set up for BFCM," not as gaps.

## Fit to capacity

Rough effort per item:
- Adjust an existing flow: 30-60 min.
- Build a new flow: 2-4 hours.
- Build a segment: 15-30 min.
- Build or update a popup: 1-2 hours.
- Build and QA a campaign: 1-3 hours.

Add up the included items and compare against the weekly hours from interview A4 times the weeks remaining. If it doesn't fit, cut in this order: Optional items, then Conditional items with the smallest audiences, then P3 work. Never cut Core items or suppressions. Tell the merchant what you cut.

## Confirm with the merchant

In the closing interview summary, state the counts and the notable skips in one or two lines, for example: "I'd focus on 7 flows and 7 segments. I'm skipping the spend matrix and category segments since you'd send them the same emails anyway. Want any of those back?"

## Use flow results, not just on/off

For each included flow, read its last-90-day results (PV4). Prioritize fixes by result: a flow converting well below the merchant's other flows, a channel missing from a high-intent flow where it converts better elsewhere (for example an SMS step that converts well in the cart flow but is missing from checkout abandonment), or a flow with high unsubscribes or SMS failures. A flow that is active and converting in line with its peers goes in `already_set`, with only BFCM-specific changes (sale offer, code stacking, pauses) as tasks.

## Recent buyers

Include recent buyers in sale sends: they often buy again because complementary products are on sale. S19 is "ordered in the last 7 days" and suppresses only the launch email. Don't plan price-adjustment policies; they're outside this plan.

## SMS belongs in high-intent flows only

SMS is for customers showing real purchase intent: cart and checkout abandonment, back in stock, early access, and the welcome step right after an SMS signup. Never recommend adding SMS to browse abandonment; it's too far up the funnel. If a merchant already sends SMS in browse abandonment, leave it alone and don't flag it. The build rejects any task or recommendation that adds SMS to browse abandonment.

## Always segment

Never recommend sending to the whole list. **Black Friday and Cyber Monday are the exception:** emails on those two days go to all email subscribers with no unengaged exclusion, and later emails on those days leave out people who bought earlier that day (a "Bought today" segment: ordered in the last 24 hours). Keep the unengaged exclusion on those days too when the account has a deliverability problem: recent broad sends bouncing above 2%, complaints above 0.1%, or a large import with unclear consent. The broadest audience any send gets is "All engaged contacts": every contact except the merchant's unengaged exclusion segment. Every email in the plan excludes unengaged contacts, VIP and early-access sends included.

Use the merchant's own unengaged segment if they have one (for example "Unengaged Contacts," "No opens in 180 days," or "To Be Removed"). If they don't, add a task to build one, and pick the window by how often they send: about 90 days without an open or click for weekly-or-more senders, 180 days for occasional senders. Say the definition in that task's details.

## SMS audiences

"All SMS subscribers" is fine as an SMS audience: consent is the gate for SMS, and the unengaged exclusion (built on email opens) doesn't apply. The "never the whole list" rule is for email.

## Every live flow is accounted for

Each active flow, email or SMS, either gets a BFCM task (sale wording, a pause, or a code check) or appears under "Already set." A live SMS cart flow left alone can double-message shoppers during the sale.

## Popups and codes

If a popup gives a code and the sale has a discount, add a task to check the code can't stack on the sale price. An everyday signup popup needs a defined reason to sign up (asked as a question if the merchant hasn't said), and its expected signup rate comes from the store's own non-sale history, never from sale-popup rates.

## Sales that end before Black Friday

If the offer ends before Black Friday, add a task deciding what shoppers see over Black Friday weekend: usually a restock or gift-guide email with no discount, and a site message. Monitor the sale's final day as well as its launch.

## Re-engagement sends

Send re-engagement emails to unengaged or imported contacts in batches of a few thousand over a week or more, leave out any group whose consent is unclear, and stop if spam complaints pass 0.1%.

## When SMS runs through another tool

If the merchant sends SMS through another tool but collects SMS signups in Privy's popup, add a step to confirm those signups reach the other tool with their consent.

## Don't

- Don't recommend same-day resends to non-openers.
- Don't state how many people "All engaged contacts" is unless the segment count is actually known.

## Choosing the top recommendations

The three recommendations are the changes most likely to move this merchant's sale, ranked by likely impact using their own numbers. Never housekeeping (renaming, tidying, documenting) or "keep doing X," unless keeping it reverses a real risk; those belong in the task list. A topic the merchant spent a long time on in the interview isn't automatically a recommendation, and neither is a decision they already made (it shows in the offer or the tasks).
