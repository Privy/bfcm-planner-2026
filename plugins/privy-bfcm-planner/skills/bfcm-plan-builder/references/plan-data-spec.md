# Plan Data Spec

The plan artifact has two parts:
- **The renderer** (`assets/plan-renderer.html`) is locked. It carries Privy's DESIGN.md styling, the page structure, chart logic, and the standing compliance text. Never edit it per merchant.
- **The data** (`plan-data.json`) is what you write: the review, the tasks, the send calendar, and the closing.

`scripts/build_plan.py` validates the data and injects it into the renderer. `assets/sample-plan-data.json` is a complete working example; copy its shape.

## Contents
1. The page, top to bottom
2. Where flexibility lives
3. Writing rules
4. Shopify vs Privy revenue (read this before the review)
5. Field reference
6. What the build script enforces
7. Building and publishing

---

## 1. The page is the plugin's output, stage by stage

Every section is filled by a specific stage of the workflow. If a stage produced something, it has a place on the page, and nothing appears that the stages didn't produce.

| Section | Filled by | Data fields |
|---|---|---|
| Top band: title, dates covered, days to Black Friday, tasks done, due this week | Stage 1 (orient), computed | `meta`, `window`, `tasks` |
| **Starting point: Daily Store Revenue** chart (lemon on the brand band, tooltips, no total) | Stage 2 pulls SH13 (or PV10 on other platforms) | `review.daily` |
| **Starting point: BFCM [year] at Privy** card (credited revenue, email vs. SMS and campaigns vs. flows bars, optional callout) | PV9, PV5 | `review.channels`, `review.callout` |
| **Starting point: Today at Privy** card | Stage 3 store snapshot: PV2, PV3, PV4, PV7 | `today` |
| Top recommendations (locked title and description): numbered list, change first, evidence under it, task link on the right | Stage 4 findings | `review.findings` |
| Your offer | Interview module B | `sale`, `window` |
| Goals | Interview A2 (merchant's own goal) plus goals the merchant controls | `goals` |
| Tasks, by week or by area | Stage 5: every included item with status, priority, evidence, owner, due date, and how | `tasks` |
| "Already set" and "Skipping" lines per area | Stage 5 items marked Ready, and the selection rules' skips | `already_set`, `scope` |
| Open questions as tasks | "Not sure" answers, as a task with status `question` | `tasks` |
| Send calendar, grouped by day | Interview module G and best-practice cadence | `sends` |
| More help from Privy (locked links) and closing | Renderer, plus `closing` | `resources`, `closing` |

Areas match the Privy checklists: Offer and codes, Flows, Displays and list growth, Campaigns, Segmentation and list health, Site and tech, Compliance and deliverability, Reporting and wrap-up.

## 2. Where flexibility lives

| Locked (renderer decides) | Flexible (you decide per merchant) |
|---|---|
| DESIGN.md look, section order, the two views, chart and list formats | Every task: text, date, owner, area, status, priority, evidence, and the how |
| The top band, texting-hours note, resource links | Starting-point stats and findings; goals |
| Area names and order; status and priority wording | Which tasks exist (fit to the team's capacity); the optional margin, store, top-seller, and popup pieces |

**Keep it concise:** about 20-30 tasks. Task text is the action, in 110 characters or fewer; setup specifics go in `detail`, shown under the task. Items that are already fine go in `already_set`, not in tasks.

## 3. Writing rules

### Writing for merchants

Every word in the plan is read by a busy merchant, not a marketer. The build catches some mistakes; the rest is on you.

- **Write it the way a Privy CSM would say it on a call.** Read each line aloud. If it sounds like a slide or a telegram, rewrite it.
- **A recommendation's headline is a complete instruction:** a verb, what to do, and who or when. "Send your big sale emails to your whole list," not "Keep peak days for everyone."
- **Its evidence is one plain cause-and-effect sentence** that leads to the headline. At most two figures, and each one says what it is ("brought in $18,240," "bounced," "turns 0.2% of messages into orders").
- **One idea per recommendation.** If it needs "and the rest to...", the second half goes in the task's details.
- **Quote the merchant's names exactly as Privy shows them.** Flow, segment, display, and campaign names are never renamed, reworded, or tidied, even when they say "Text" or look odd ("Welcome Series (Copy)" stays as is). List every name you quote in `meta.proper_names`; the wording checks skip text inside those names, and names in `scope` and `already_set` count automatically.
- **Use the merchant's own names, or plain descriptions.** Their segment and flow names ("Engaged 180," "Welcome Series"), or "your sports-fan segments." Never labels you made up ("peak days," "fan segments").
- **The line under a heading adds something.** It never repeats the heading in other words.
- **Say what each number is.** "Sent to," "opened," "brought in." Don't round in headlines (59% stays 59%). Write ranges with "to": "$6,400 to $10,400."
- **Punctuation:** no em dashes anywhere, including message copy. No semicolons in plan wording; use two sentences. Avoid "yet" and "vs." in recommendations; say how the two facts connect.
- **Deadline wording names the time, not a time zone:** "the sale ends tonight at 11:59pm." We don't know each contact's time zone.
- **SMS can go to "All SMS subscribers";** the unengaged exclusion is for email.
- **Never say "everyone" or "whole list."** The broadest audience is "All engaged contacts," and its "Exclude:" line names the merchant's unengaged segment. **Black Friday and Cyber Monday are the exception:** their emails go to "All email subscribers" with no unengaged exclusion, and every later email on those days excludes "Bought today" (people who ordered earlier that day). Accounts with a deliverability problem (`meta.deliverability_risk: true`: recent broad sends bouncing above 2%, complaints above 0.1%, or a large unvetted import) keep the unengaged exclusion on those days too. Past sends can be described as "broad" or "sent to more people," not as "full-list."
- **Unsubscribes are rates, never counts.** "0.8% unsubscribe," not "92 unsubscribes." About 0.2% is typical.
- **Prepared early, live later.** A task that builds sale content before the sale says when it goes live and when it switches back.
- **Name the dates, not "last 90 days."** "From Privy, Jul 3 to Sep 30," because merchants compare the page with a dashboard whose rolling window has moved on since the plan was built.
- **Dates go in parentheses after the figure they qualify:** "$41,300 from SMS (Jul 3 to Sep 30)," "2,140 orders (Nov 20 to Dec 5)." Never tack a date range on after a comma. Inside a full instruction sentence, plain "from Nov 24 to Dec 4" is fine.
- **Comparisons name both periods** ("down from 2.3% the 90 days before," "down from 1.3% during last BFCM"). The "Today at Privy" card shows current numbers only, with no up or down.
- **The signup rate is per popup view, not per visitor.** Say "2.0% of popup views lead to a signup," never "of visitors." One visitor can see a popup on several pages.
- **Say "your popups" for the overall signup rate.** Most merchants run several; name a single display only when you mean that one.
- **Headings name what's there.** "What you keep at each tier," not "Use last year as a baseline, not a promise." No slogans, maxims, or "X, not Y" lines.
- **Platform wording follows `meta.platform`.** "Set up the discount in BigCommerce" for a BigCommerce store; never name Shopify, its apps, or its features (like Buy X Get Y) for a store on another platform, except to explain why something isn't available.
- **Never assume what the store sells.** Product focus comes from top-seller data or from the merchant's answer.
- **Counts in headings match the calendar.** "9 emails and 4 SMS" means exactly that many rows.

Before and after:

| Before | After |
| --- | --- |
| Keep peak days for everyone, fan segments in between. *Fan emails open at 66%, yet September's full-list sale email still made the most of any send.* | **Send your big sale emails to your whole list.** Your sports-fan segments open more emails, but in September an email to your whole list still made the most money. |
| Send more emails, to Engaged 120 rather than everyone. *Four BFCM emails brought in $18,240. The smaller sends bounced 0.4-0.5%; the full-list ones up to 2.3%.* | **Send more sale emails, but only to Engaged 120.** Last year's four sale emails brought in $18,240, and the ones sent to your full list bounced more. |
| 9 emails and 4 SMS, with everyone on the three biggest days. *Everyone on the three biggest days, the fan segments in between.* | **9 emails and 4 SMS.** Launch day, Black Friday, and Cyber Monday go to your whole list. The days in between go to your sports-fan segments. |


These follow `assets/privy-DESIGN.md`.
- **Headings state the claim** ("25 tasks between now and Saturday, Dec 5"), not the genre ("The plan").
- **No internal codes on the page.** Checklist IDs (F05, S19, R47) stay in the data for validation; the page shows segment and flow names instead, and owners as "Owner: [name]".
- **Don't explain compliance rules in the plan.** Deadline and texting rules are enforced by the build; the page just follows them.
- **Nothing from the plan at the top.** The opening band is generated from the store name, dates, and progress. The offer appears in the sale phase, where it has context.
- **No forecasts or targets.** The review is what happened; goals are steps the merchant controls.
- **Findings pair an observation with a response.**
  - The observation is a fact with its source.
  - The response is what this year's plan does about it, linked to a task.
  - Never "you'll make more because."
- **Send timing.** The calendar shows the time of day (morning, late morning, early afternoon, late afternoon, evening), never clock times or time zones; we don't know each contact's time zone. Keep exact `time` values in the data for ordering and checks. Privy holds any SMS that would land in quiet hours until they end, and merchants can send by each contact's time zone, so recommend timezone-based sending with a task. The scheduling task tells the merchant to pick exact times a few minutes off the hour. Every SMS carries a shop link (`[link]` placeholder).
- **Times live in the calendar only.** Don't write send times into task text or details; the build rejects a task whose time doesn't match that day's sends.
- **Recent buyers are good people to include.** Leave out only people who bought in the last 7 days (S19), and only from the launch email. They often buy again because complementary products are on sale.
- **Warm-up steps are tasks.** Each warm-up step has a campaigns task on its date.
- **Ramp up before the sale.** At least two regular sends to engaged contacts in the 5 weeks before the first sale send, one of them 2+ weeks out.
- **A sale-period display.** A displays task in the 10 days before the sale puts a sale popup or bar live for the whole sale, and the wrap-up switches it back.
- **Monitoring covers every channel the plan uses:** SMS opt-outs as well as email complaints, bounces, and unsubscribes. Don't include SMS delivery failures: they're often landlines, and merchants can't see or remove them.
- **Grow the SMS list** when the plan sends SMS: an SMS signup step on the popup, with Privy's consent wording.
- **Send copy matches the terms.** Never feature an excluded item in a send, and don't say "everything" when the terms exclude anything beyond gift cards.
- **Nothing says the sale is live before it starts.** Only sends on or after `window.early_access_start` may say so before `offer_start`.
- **Launch-morning check.** Every plan has a site or offer task on the launch date: pricing live, exclusions holding, one test order, before the first sale send.
- **Size tasks for one person.** Split writing sends from scheduling and previewing them. Monitoring is one task per peak day (launch, Black Friday, Cyber Monday), never "after every send."
- **Sender authentication means SPF, DKIM, and DMARC, plus the sending domain in Privy,** not DMARC alone.
- **Label what a number is.** A send's recipient count is "sent to," not list size or "reach." Don't round figures in headlines (59% stays 59%).
- **Two launch checks.** The day before anyone sees sale pricing (early access included), a full check: the discount is scheduled with the right dates and exclusions, popups and flows are set to switch on, and a test with a hidden code that has the same settings passes. On launch morning, a quick confirmation that sale prices are showing before the first send. The sale starts 30 minutes to 3 hours before the first sale email, so email isn't held back once the sale is live.
- **Sale-day sends go out on the store's clock** (`store_time: true` on the row): every send from the first day shoppers see sale pricing, early access included, through the end of the sale. Timezone-based sending is only for pre-sale sends, so everyone hears the sale is live, or ending, at the same moment. 
- **Every segment the plan builds gets used by a send** (suppression segments aside). If none does, drop the build.
- **Owners come from the team** when the merchant named one; "You" only when they didn't.
- **Plans that send SMS include a Black Friday SMS and one in the final 24 hours.**
- **Don't ask the merchant to research Privy.** Look capabilities up in the help center and skip what isn't available, with the reason.
- **Say SMS, never "text" or "texts,"** everywhere the merchant reads: "SMS subscribers," "an SMS step," "email and SMS." The build rejects "text" or "texts" in plan wording.
- **Task text starts with a verb** naming the action ("Update the abandoned cart flow...", "Send the teaser..."), never a noun label ("Abandoned cart: ...").
- **Plain, specific, second person.** No hype words or exclamation points. Privy vocabulary: displays, flows, campaigns, contacts and subscribers, SMS.
- **Dates are ISO; times are 24h.** The renderer formats them.
- **Send copy is the merchant's voice** (subject and message). Every claim must be true on its send date.
- **SMS messages use straight quotes and plain punctuation.** Curly quotes, ellipses, dashes, and emoji switch an SMS to UCS-2 encoding, which cuts one message from 160 to 70 characters. The page shows SMS copy exactly as written; elsewhere it applies smart punctuation automatically.

## 4. Shopify vs Privy revenue

The two systems book revenue on different days:
- **Shopify** records revenue on the **order date**.
- **Privy** attributes an order to the **send date** of the email or SMS that drove it.

Totals across the whole window roughly agree. Day by day they don't: a Cyber Monday email's revenue lands on Monday in Privy, but some of those orders land Tuesday in Shopify.

Rules:
- The daily chart is Shopify only (order date). Its rows allow only `date` and `revenue`.
- Channel revenue (flows, email campaigns, SMS) comes from Privy as window totals only. There's no daily channel data anywhere in the plan.
- Don't write findings that compare a day's channel revenue with a day's store revenue ("Friday's email drove $41K"). Use window totals ("SMS drove $27.4K over the window").
- Any share like "email and SMS were 40% of revenue" mixes the two systems. Label it approximate, or leave it out.
- For live monitoring steps: compare Shopify to Shopify by day, and check Privy per send.

## 5. Field reference

Required unless marked optional. `assets/sample-plan-data.json` shows every shape.

**meta:**
- `store_name`, `store_domain`
- `prepared_date`: the date this version was built, shown as "Last updated". Set it to today on every update.
- `timezone` and `tz_label`
- `profile`: `returning` | `switched` | `new_store`
- `gmv_band`, `has_csm` (true when the merchant works with a Privy CSM)
- `privy_scope` (optional): `full` (default) or `displays` for merchants who use Privy only for displays. Display-only plans have no send calendar, no warm-up requirement, and no send-related checks; the plan covers displays, signup capture, and the site.
- `email_limit` (optional): the merchant's email pace from the interview, `{"per_day": N}` or `{"every_days": N}`. Every email in the calendar must respect it.
- `proper_names` (optional): every merchant flow, segment, display, or campaign name quoted in the plan, exactly as Privy shows it.
- `timezone_sending` (true when the plan recommends sending SMS and emails by each contact's time zone)
- `currency` (ISO 4217, e.g. `CAD`) and `platform` (`shopify`, `bigcommerce`, `wix`, `weebly`, `other`)
- `privy_first_send` and `privy_last_send`: dates of the first and most recent Privy email or SMS (null if none). They decide whether a warm-up is required.
- `team`: owner names the merchant gave in the interview. Every task owner must be one of these, "You", or "Your Privy CSM" (only if `has_csm`).

**window:** `black_friday`, `offer_start`, `offer_end`, `extension`, and `early_access_start` (the date early access opens, when there is early access). The build uses `early_access_start` for the launch checks and sale-day rules. It never guesses from campaign names, so a teaser called "Early access starts Saturday" is just a teaser.

**sale:** `headline` and `terms`, shown as "Your offer."

**review** (optional; not allowed for `new_store`):
- `daily` (optional): store orders by order date, `source` Shopify (preferred) or Privy (store totals, other platforms). Each day has `date`, `revenue`, and optional `orders` (shown in the tooltip). Optional `highlight` (`start`, `end`) marks last year's actual sale; optional `peak_label` (20 characters max) names the best day, which otherwise reads "Black Friday," "Cyber Monday," or "Best day." Titled "Daily Store Revenue - BFCM [year]," with the legend "Order Revenue ([platform])." No total is shown, so store revenue is never compared with Privy's.
- `channels` (optional): `source`, `basis`, `total`, and optional `by_channel` (`email`, `sms`) and `by_type` (`campaign`, `flow`). Privy uses `send_date`, or `attribution_date` with the total only before Privy's reporting boundary. Merchant-reported uses `as_reported`.
- `callout` (optional, needs `channels`): `figure` (16 characters max) and `text` (90 max), a Privy figure worth noticing, such as "CA$44,751 came from just two VIP early-access emails."
- `findings` (up to 3): `change` (the headline, 80 characters max), `observation` (one line of evidence, 160 max), `source`, `task`, and optional `task_label` (40 max) for the link.
- `stats`: no longer shown; optional.

**today:** `as_of` (within two weeks of `prepared_date`) and `stats` (2-4). **The first two are always total mailable and total textable** (PV2), with `text` exactly "Total mailable contacts" and "Total textable contacts" (Privy's own terms; "textable" is the one exception to "say SMS"). Show 0 when a merchant has no SMS subscribers. The other one or two are the most useful current Privy figures. Each stat has of `label`, `value`, `caption`, `source` (`Privy` or `Shopify`), `basis` (`count`, `rate`, `order_date`, or `send_date`), and `text`: the short phrase shown beside the number (70 characters max), such as "people got your last full-list email, Sep 26." Shown in the "Today at Privy" card.

**goals:** optional `merchant_goal` (only if volunteered, in their words), and `items` of `goal`, `by`, `check`.

**plan:** `title` and `lede`.

**tasks:** each with
- `id`, `date`, `text`, `owner`;
- `category`: `offer` | `flows` | `displays` | `campaigns` | `segments` | `site` | `compliance` | `reporting`;
- `status`: `update` | `missing` | `unknown` | `question` (open question). Shown as a badge at the right of the row, after the area badge (week view only);
- `priority`: `P1` (before the first BFCM send) | `P2` (before launch) | `P3` (if time allows);
- `evidence`: `privy` | `shopify` | `merchant` (you told us) | `recommended` (Privy recommends). `owner`, `priority`, and `evidence` are checked by the build but not shown on the page;
- optional `detail`: setup specifics shown under the task, only when needed (settings, rules, codes, dates, thresholds, counts). Not reasons (those go in findings) and not pointers to other sections. `ref` (checklist IDs, never shown) and `done` are also optional.

**already_set** (optional): `category`, `name`, optional `ref`. For items stage 5 marked Ready.

**warmup** (required when there's no Privy sending history, the first Privy send was under 90 days ago, or nothing has been sent in the last 30 days, whatever the profile): `intro`, and `steps` of `audience` and `from`. A merchant who switched months ago and sends steadily doesn't need one; a merchant who was on Privy last BFCM but went quiet does.

**sends:** `title`, `lede`, and `rows` of `date`, `time`, `channel`, `campaign`, `audience`, `suppress`, `subject`, `message`. Grouped by day on the page, with Thanksgiving, Black Friday, Small Business Saturday, Cyber Monday, and extension days labeled. Each send shows a channel icon (envelope for email, speech bubble for SMS, with the name for screen readers), its time of day, the message, and "Include:" and "Exclude:" audience lines. Optional per row:
- `deadline_ref`: the end datetime a deadline claim refers to ("ends tonight"); required for deadline wording, which may only run in the final 24 hours.
- `store_time: true`: the send goes out on the store's clock rather than each contact's time zone. Required on deadline sends when `meta.timezone_sending` is on.
- `distinct_offer`: true when a send announces an offer different from the main sale.
- `inventory_backed: true`: required for scarcity wording, checked against live stock at send time.
- `post_sale: true`: a plain follow-up after an early-ending sale (a gift guide or restock note). Allowed through Cyber Monday, and its wording can't mention a sale, discount, deal, or free gift.

**scope:** `segments` and `flows`, each with `included` (`id`, `name`) and `skipped` (`id`, `name`, `reason`).

**basis** (optional, not shown on the page): `data` (sources and date ranges, plus any partial-data notes) and `assumptions`. Kept in the plan data so Privy's team can audit where numbers came from.

**resources** (optional, up to 3 extra, privy.com only), **popups** (popups-only plans; see "Optional pieces" below), **closing** (optional: `date` of the next check-in, which the planner mentions in chat; it isn't shown on the page).

## Standard tasks the build adds

Don't write these. Before checking a plan, the build adds each one the rules require, unless the plan already has a task that meets the rule (or it's listed under `already_set`). Each uses a fixed ID, so checkmarks stay attached across rebuilds, with the date, platform name, and owner (`meta.area_owners`, by area, else "You") filled in:

- `t-std-discount`: set up the sale discount, scheduled with the sale. `t-std-stacking`: check codes can't stack on it.
- `t-std-precheck` and `t-std-golive`: the full check the day before sale pricing, and the quick check that morning.
- `t-std-display-sale`: the sale popup and announcement bar. `t-std-bfweekend`: Black Friday weekend, when the sale ends before it.
- `t-std-tzsend` (with timezone sending) and `t-std-schedule` (when there are sends).
- `t-std-recentbuyers` and `t-std-boughttoday`, when the calendar uses those exclusions.
- `t-std-watch-launch`, `-bf`, `-cm`, and `-final`: monitoring on each of those days that falls in the sale.
- `t-std-undo` and `t-std-recap`: switching things back, and the mid-December recap.

To word one differently, write your own task that meets the rule; to drop one, list its ID in `meta.skip_standard_tasks`. A plan's "N tasks" heading is recounted after they're added.

## 6. What the build script enforces

Read this before writing any plan data. Errors are the rules that protect the merchant: they block the build. Style and wording checks are warnings: they're reported, but never block. Errors name tasks by ID, never by position.

**Errors** (nothing is built until fixed)

*Structure*
- Required fields, valid enums and IDs; dates inside the plan window; unique task IDs; every finding points to a real task.
- With `--previous`, an existing task ID reused for a different task.

*Launch and timing*
- A full check the day before anyone sees sale pricing (`window.early_access_start`, else `offer_start`), and a quick check on that morning.
- The sale goes live at least 30 minutes before its first sale email (a warning past 3 hours).
- With timezone sending on, every send from the first day of sale pricing through the end has `store_time: true`.
- A popups or bar task in the 10 days before the sale.
- If the offer ends before Black Friday, a task for what shoppers see that weekend.
- Offer words match the dates ("through Cyber Monday" ends on Cyber Monday).
- Nothing after the sale ends, except `post_sale: true` sends by Cyber Monday with no sale, discount, deal, or free-gift wording.
- The merchant's email pace (`meta.email_limit`): no more emails per day, and no closer together, than they asked.

*Audiences*
- No "everyone," "whole list," or "all contacts." "All email subscribers" only on Black Friday and Cyber Monday.
- Every other email excludes unengaged contacts (S20), and Black Friday and Cyber Monday too for `meta.deliverability_risk` accounts.
- Later emails on Black Friday and Cyber Monday exclude "Bought today."
- S19 (recent buyers) excludes only the launch email.
- No SMS added to browse abandonment.

*Accuracy*
- Shopify wording only for Shopify stores. "Today at Privy" opens with "Total mailable contacts" and "Total textable contacts" and shows Privy figures only.

*Truthful claims*
- Deadline language only in the real final hours; scarcity needs `inventory_backed`; SMS between 9:00 and 20:00.
- No forecasts, competitor names, or customer emails and phone numbers.

**Warnings** (never block the build; fix them in the same pass when you can)
- Wording: em dashes, semicolons, "text" instead of "SMS," "coach" instead of "Privy CSM," unsubscribe counts instead of rates, "of visitors" for the signup rate, "last 90 days" instead of named dates, "up" or "down" in Today at Privy, hype words, slogan headings.
- Counts: send or popup heading counts that don't match the calendar; "Make it yours" with other than 3 or 4 ideas, ideas over 90 characters, or ideas starting "Write" or "Draft." 
- Semicolons; date ranges tacked on after a comma.
- Recommendations: more than two figures of evidence, starting with "Keep" or "Rename," or mentioning Privy-side issues (stale counts, sync delays).
- No discount-setup task; no final-day monitoring; sales live more than 3 hours before the first email.
- Prep tasks without a go-live date; task counts outside 8 to 35; scope items no task uses.

## 7. Mobile and PDF

The page is built for phones: nothing scrolls sideways, the send calendar becomes cards, tap targets are at least 22px, and the nav keeps the current section in view.

Nav links and recommendation task links scroll smoothly to their target, landing just below the sticky nav (instantly for viewers who've set their device to reduce motion). The nav has a light/dark toggle on the right. The page starts on the viewer's system setting, remembers their choice in their browser, and prints in light mode either way.

For a PDF, the print layout:
- hides the nav and view toggle;
- prints the week view, with task details included;
- forces the light theme;
- keeps task rows and send rows from splitting across pages.

Merchants can print from the browser. When they ask for a file, build one with `--pdf` (below) and present it.

## 8. Building and publishing

1. Write `plan-data.json`.
2. Run `python3 scripts/build_plan.py plan-data.json "/mnt/user-data/outputs/[store]-bfcm-plan.html"` from this skill's folder. Add `--pdf "/mnt/user-data/outputs/[store]-bfcm-plan.pdf"` when the merchant wants a PDF. It uses Playwright if installed; otherwise it says so and the merchant can print to PDF from the browser.
3. Fix every error and re-run. Fix the warnings that apply.
4. Publish the built HTML as an artifact. To update a plan, edit the data, rebuild, and republish to the same artifact.

**Without code execution:** copy `assets/plan-renderer.html`, replace `/*PLAN_DATA*/` with the JSON, and check section 6 by hand. Check especially the attribution rules, every deadline phrase against the real end time, SMS times, and the absence of forecasts and competitor names.

**Chart label.** The daily revenue chart says "Order Revenue (Shopify)" only when `review.daily.source` is `Shopify`, meaning the figures were pulled from the merchant's Shopify connection. Figures from Privy's copy of the store's orders are labeled just "Order Revenue."

**Revising a plan.** Task IDs are permanent: progress (checkmarks) is stored against them. When revising a plan, keep every existing task's ID, even if its wording or date changes. Give new tasks new IDs, and never reuse an ID for a different task. Drop a task only when it no longer applies, and tell the merchant. Build with `--previous OLD.json` so the build flags removed or repurposed IDs.

**Shared progress.** A plan published with the `db` and `user` capabilities saves checkmarks to its own database, in collection `progress`: one record per task ID, `{"done": true|false, "by": <viewer id or "planner">, "at": <epoch ms>}`. Everyone who can open the plan sees the same progress. A done task is crossed out; who ticked it and when are stored for the planner but not shown. The merchant can share the plan with anyone (teammates, freelancers, their Privy CSM), including invited guests outside their organization. Anyone given edit or contributor access can tick items; view-only viewers see progress but can't change it. Without the runtime (a downloaded copy or PDF), checkmarks save in that browser only, and the page says which mode it's in. A task's `done` field in plan-data only sets its starting state before anyone has ticked it.

**Shared progress on other hosts (a ChatGPT Site).** In Claude, the page uses Claude's database and user capabilities. Anywhere else, the host supplies them through one hook, set before the page's script runs: `window.planProgress = { db, user }`, implementing the same small interface:
- `db.collection("progress").onSnapshot(callback, onError)`: calls `callback({ docs: [{ id, data() }] })` with every record, now and on each change; `db.collection("progress").doc(taskId).set({ done, by, at })` returns a promise and rejects with `{ code: "permission_denied" }` for view-only viewers.
- `user.id()` returns the viewer's ID (a promise), and `user.profiles(ids)` returns `{ id: { name } }`.

This adapter is the only addition the page allows; never change the renderer itself. Without a hook or Claude's capabilities, checkmarks save in that viewer's browser.

**remix:** 3 or 4 requests the merchant could make of their agent, specific to this plan (90 characters at most each), shown first under "Make it yours" above the fixed ideas. Write them as the merchant would say them: "Write the VIP early-access email for Nov 24." Base them on this plan's sends, findings, and products. Never suggest the agent changes the store or Privy (no "set up," "create," or "turn on"), and never offer to write campaigns (no "write" or "draft"): it's an insight tool, so phrase ideas as questions about strategy, timing, audiences, or what a send should lead with.

**Disclaimer.** Every plan ends with this locked disclaimer, in Privy's approved wording; the date is the plan's `prepared_date`. Change it only in the renderer:

> This plan was generated by the Privy BFCM Planner using AI, based on your Privy data, any other services you connected, and the information you provided as of {date}. The Planner only uses aggregate Privy data and does not make changes to your Privy account or any other connected service. The plan is for informational purposes, may contain errors, and does not guarantee results, so please review all figures, offers, and dates before acting on them. It is not legal advice. You are responsible for making sure your marketing and promotions comply with applicable laws, including those on consent, messaging hours, and promotional claims. Use of the Planner is subject to Privy's [Terms of Service](https://www.privy.com/terms-of-service) and [Privacy Policy](https://www.privy.com/privacy) and the terms of the AI platform you use to access it.

**Channel labels.** Each send is labeled "Email" or "SMS" next to its icon.

**Privy CSM, never "coach."** The person at Privy who works with the merchant is their Privy CSM.

## Optional pieces

These fit into the page's existing sections. Their headings are fixed, so the plan never writes one.

| Data | Where it appears | Add it when |
|---|---|---|
| `sale.margin`: `rows` of `{tier, keep}` plus an optional one-line `note` (140 characters at most) | Inside the "Your offer" box, one line per tier: "Spend $100, save 15% · You keep $20 on a $100 cart" | The margin check ran (tiers, or a discount of 25% or more). Include Cyber Monday tiers |
| `review.store_totals`: `{total, orders, from, to, source}`, optional `split: {a_label, a, b_label, b}` | A "BFCM 2025 at your store" card in "Where you're starting" | There's no daily chart but last year's store totals exist |
| `review.top_sellers`: up to 5 of `{product, in_stock, sold_last_bfcm, backup}` | A "Your top sellers" card in "Where you're starting"; "Could sell out" shows when stock is at most twice last BFCM's sales | Shopify inventory is available |
| `popups`: `title`, `lede`, `rows` of `{start, end, kind (popup, bar, or embedded), name, offer, audience}` | A "Popups" section in place of Sends, grouped by start date | The merchant uses Privy for popups only. The title counts popups: "3 popups and a bar, starting Oct 5" |

## Task views and labels

The task list has four views: By week (default), This week (due this week, then next week), By area, and Calendar (one month at a time, with arrow buttons to move between months; it opens on the current month; clicking a task opens its details and a Done checkbox). Each task shows one badge: its area (Flows, Compliance, and so on). Priority and status stay in the data for ordering and checks, but aren't shown.
