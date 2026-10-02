# Interview Bank

Ten modules. **Essential** modules run in both Quick and Full plans; **Full** modules run only in Full plans (but still run their deep dives if a trigger fires from earlier answers or data). Skip any question the Shopify/Privy data already answers; confirm instead of asking.

Format per question: the question, tappable options, and what the answer feeds. **At most 4 options per question** (the limit of Claude's tappable tool), with "Not sure" counting as one of the four when it fits; mark questions where several answers can apply as multi-select; record "Not sure" answers as open items using the matching readiness question (R##) as the team follow-up.

Deep dives: ask them only when the trigger fires. Open each deep dive with one sentence on why it matters.

---

## Module K: New to Privy (Essential when the merchant wasn't on Privy for last year's BFCM)

Questions K1-K4 live in `new-to-privy.md` section 7. Ask them right after Module A, since they change baselines, segments, and cadence.

## Module R: Last BFCM (Essential for returning and switched merchants)

Ask after the snapshot, once you've shown last year's numbers.

R1. Anything about last BFCM the data won't show? A stockout, a site issue, a shipping delay, or a send that went wrong?
Options: Yes, something happened / Not that I remember
Feeds: review findings (as merchant-reported, with the source saying so).

R2. What would you keep, and what would you change?
Options: Mostly repeat it / Change a few things / Start fresh / Skip
If they pick "Change a few things," follow up: "What would you change?" This is one of the few typed answers.
Feeds: review findings and the steps that respond to them.

## Module A: Goals and team (Essential)

A1. What does a great BFCM look like for you this year?
Options (multi-select): Beat last year's revenue / Grow the list and new customers / Protect margin / Clear inventory
Feeds: plan emphasis and the goals the merchant controls.

A2. (If Shopify gave last year's numbers) "Last year you did $X Thanksgiving through Cyber Monday and $Y in the four days after. Do you have a revenue goal for this year you'd like me to track against? Totally optional."
Options: Yes, I'll share it / No set goal
Feeds: the merchant's own goal, recorded and labeled as theirs. Never suggest a number or a growth percentage.

A3. Who's doing the work between now and launch?
Options: Just me / Me + one marketer / In-house team / Agency or freelancer
Feeds: scope cut, owners.
A3a. Who owns each area? (Offer and codes, flows, displays, campaigns, segments, site and tech, compliance, reporting.) A first name, or "me" for yourself.
Feeds: meta.team and task owners. Don't invent names; unassigned areas are owned by "You".
A3b. (Skip if Privy data shows it.) Do you work with a Privy CSM?
Options: Yes / No / Not sure
Feeds: meta.has_csm. Only then can steps be owned by "Your Privy CSM" and the closing offer a session with them.

A4. Hours per week available for BFCM prep?
Options: Under 3 / 3-8 / 8-15 / 15+
Feeds: scope cut.

**Deep dive: big ambitions, thin team** (the merchant shares a goal well above last year, or lists many priorities, with "Just me" or under 3 hours a week)
- Which one or two channels drive most of your revenue today?
- What could you stop doing in November to free up time?
Outcome: a ruthless P1-only plan focused on the few actions most likely to matter. Don't comment on whether their goal is achievable.

## Module B: Offer and economics (Essential)

B1. Have you decided on your BFCM offer?
Options: Yes, locked / Have ideas / No idea yet
B2. What type? (if decided or leaning)
Options: Percent off sitewide / Tiered spend-and-save / Gift, bundle, or BOGO / Something else (free shipping, a mix)
B3. Discount depth?
Options: Under 15% / 15-25% / 25-40% / 40%+
B3a. **Margin check (Essential, Quick plans included) when the deepest discount is 25% or more, or when tiers are involved.** Ask one question: "What's your contribution margin on a full-price order? That's what you keep after product cost, shipping, and fees."
Options: Under 30% / 30 to 50% / Over 50% / Not sure
Invite an exact number ("or type your exact number"), since the math is more precise with one; with a range, use its midpoint and say so. Then show a small table of what they keep per order at each tier (contribution margin minus the discount, times the cart value). Flag any tier where a bigger cart keeps less than a smaller one, or where they keep nothing, and offer adjusted tiers. Label the result as based on their number.

B3b. **Product focus (Essential when there's no Shopify top-seller data; otherwise confirm).** "Which products or collections do you want to lead with this year?" With Shopify data, confirm instead: "Last BFCM your top sellers were X and Y. Lead with those again?" Never assume a product focus, a new launch, or a category from the store name or a guess.
Feeds: send subjects and messages, the stock check, remix ideas.

B4. Early access for VIPs and signups?
Options: Yes, 24h / Yes, 48h / No / Not sure
B5. Is Cyber Monday the same offer or a new one?
Options: Same offer all the way through / A new Cyber Monday offer / Not decided
B5b. Will you extend the sale through Friday, Dec 4?
Options: Yes, extend it / No extension / Not decided
If "Not decided," explain in one sentence why it has to be decided before launch: if the same deal continues past Monday, Monday's emails and SMS can't say it's ending. Mark it P1 with a due date before the first "ends" message is written.
Feeds: R24, R28, F03.

**Deep dive: margin** (B3 is 25%+, or merchant wants to "protect margin," or offer undecided)
- Roughly what's your gross margin overall, and on your top 3 BFCM products?
- What does an order cost you to pick, pack, and ship?
- What's your typical return rate?
- Any products that should never be discounted?
Outcome: margin-tiered offer recommendation (best-practices section 4) with a simple contribution-margin check per order at each tier.

**Deep dive: stacking** (Shopify/Privy shows active codes in welcome, popup, SMS, cart, birthday, or win-back)
- Show the list of live codes found. For each: pause, replace with BFCM offer, or allow to stack?
- Are influencer or affiliate codes running in November?
Outcome: stacking table in the plan; F01, F02, F04, F05, F15 actions.

**Deep dive: undecided offer** (B1 = No idea yet)
- What sold best last BFCM (show SH5)? Any overstock you want to move?
- Do customers buy multiples or gifts?
Outcome: two or three offer options with trade-offs; ask the merchant to pick one.

## Module C: Dates and logistics (Essential)

C1. When does the public sale start and end? (date, time, time zone)
Options: Fri Nov 27 12:00am / Thu Nov 26 (Thanksgiving) / Earlier week-long / Custom
C2. What delivery times will you promise BFCM buyers?
Options: Known / Not yet
C3. Any inventory worries on hero products? (show sellout-risk flags from SH5)
Options: We're covered / Some risk / Big risk
Feeds: R25, R27, R08, R36.

**Deep dive: inventory risk** (sellout flags or C3 = risk)
- Can you reorder in time? Which products are the fallbacks?
- Should Back in Stock (F07) waitlists be promoted?
Outcome: hero and fallback product list; product-block guidance for flows.

## Module D: List growth and on-site (Essential)

D1. (Show PV3 live displays.) Which of these should change for BFCM?
D2. How will people sign up for early access?
Options (multi-select): Popup / Embedded form / SMS keyword / Social
D3. Any spin-to-win or gamified popup?
Options: Yes / No
D4. Separate experience for returning subscribers?
Options: Yes / No / Not sure
Feeds: R16-R22.

**Deep dive: slow list growth** (PV2 shows flat or declining 90-day growth, or SMS list under ~10% of email list)
- Where does most traffic land (homepage, collections, product pages)?
- Current popup offer and delay?
- Promoting signups on social or in paid ads?
Outcome: display plan with specific placements, timing, and an SMS two-step capture.

## Module E: Flows (Essential; details from data)

Mostly answered by PV4. Confirm only:
E1. (Show flows found and their status.) Anything I'm missing, like flows in another tool?
E2. Should lapsed customers get the BFCM offer, or should Win-Back stay paused until the sale ends on Dec 4?
Options: Include in BFCM / Pause until Dec 5
E3. (Only ask what the data didn't show.) Do you have a loyalty/VIP program, collect birthdays, sell consumables people reorder, or use a back-in-stock waitlist?
Options (multi-select): Loyalty or VIP program / Birthdays / Reorders or back-in-stock waitlist / None of these
Feeds: which Conditional flows apply (selection-rules.md).
E4. What should brand-new BFCM buyers hear first?
Options: Brand story / Best sellers / Second-purchase offer
Feeds: F01-F15, R12, R14.

**Deep dive: abandoned cart** (F05 missing, off, or includes its own discount)
- Does the cart flow include a discount? Keep it during the sitewide sale?
Outcome: F05 rebuilt timing (30-60 min first touch, SMS step, sale-ends touch).

## Module F: Segments and audiences (Full)

F1. (Show proposed VIP threshold and size from SH8.) Does this definition fit how you think about VIPs?
Options: Yes / Higher bar / Lower bar / We use a loyalty tier
F2. Main product categories to segment by? (show SH10)
F3. Run a subscription program?
Options: Yes (Recharge or similar) / No
Feeds: S01-S20.

## Module G: Campaign calendar (Full; Essential if under 28 days out)

G1. How many emails and SMS did you send last BFCM? (confirm from PV5. If the merchant is new to Privy, skip this and use module K in `new-to-privy.md`.)
G2. Comfortable with 1-2 emails a day to your most engaged subscribers during peak days?
Options: Yes / Keep it lighter / Heavier
G3. If you extend, what changes in the extension (new offer, new products, or the same deal with a clear end)?
Options: Same deal, firm end Fri / New angle or products / Deeper on select items / Not extending
Feeds: R23-R28 and the send calendar.
Record the answer as `meta.email_limit`, in the merchant's terms: `{"per_day": 1}` (at most one email a day) or `{"every_days": 2}` (one email every two days). The build rejects a send calendar that breaks it.

## Module H: Deliverability and compliance (Essential)

H1. Is your sending domain authenticated with SPF, DKIM, and DMARC?
Options: Yes / Not sure / No
H2. Have you checked your spam complaint rate (e.g., Google Postmaster Tools)?
Options: Yes, under 0.1% / Yes, 0.1-0.3% / Above 0.3% / Never checked
H3. Are all SMS subscribers collected with documented opt-in?
Options: Yes / Mostly / Not sure
H4. Does anyone check discount claims, end times, and countdowns before sends go out?
Options: Yes / No
If No, add a P1 claims check (best-practices section 11a) owned by whoever schedules sends.
Feeds: R32, R33, R39-R43.

**Deep dive: deliverability risk** (H1 not Yes, H2 above 0.1% or never checked, PV7 shows a large unengaged share, or the merchant is new to Privy and hasn't sent a large campaign yet)
- When did you last send to your full list? How big is the unengaged segment?
- Willing to run a re-engagement send in October and suppress non-responders?
Outcome: warm-up schedule, sunset rule, daily monitoring owner.

**Deep dive: SMS compliance** (H3 not Yes, or heavy SMS cadence planned)
- Where do SMS subscribers come from (popups, checkout, keyword, imports)?
- Any imported lists?
Outcome: consent audit step, recommended send window (9am-8pm recipient local) and 3-per-24h cap, framed as guidance to confirm with counsel.

## Module I: Site and tech (Full)

I1. Is a BFCM landing page or sale hub planned?
Options: Yes, built / Planned / No
I2. Has anyone tested checkout with every BFCM code?
Options: Yes / Will do / No
I3. UTMs and pixels verified on sale pages?
Options: Yes / No / Not sure
Feeds: R34-R38.

## Module J: Reporting and wrap-up (Full)

J1. Who watches results during the sale, and what do they check?
J2. Who owns reverting BFCM changes and the recap?
Feeds: R44-R48.

---

## Closing summary (always)

Restate in 5-8 lines: the merchant's own goal (if they shared one), offer and exact start and end times (including the extension decision), early access, core audiences, biggest changes to flows and popups, known gaps and who will answer them. Include the scope in one line: how many flows and segments you recommend and the notable skips (for example "7 flows and 7 segments; skipping the spend matrix and category segments since they'd get the same emails"). Ask: "Want any of those back, or ready for me to build the plan?"
