# Merchants New to Privy

Use this when the merchant was not live on Privy for last year's BFCM (Nov 27 - Dec 5, 2025). Determine this in stage 2 from Privy data (PV0 in `data-pulls.md`), then confirm it in the snapshot.

## Warm-up depends on sending recency, not profile

Require a warm-up when there's no Privy sending history, the first Privy send was under 90 days ago, or nothing has been sent in the last 30 days. A merchant who switched months ago and sends steadily skips it. A merchant who was on Privy last BFCM, left, and came back needs it, along with a rebuild of any displays and flows that were switched off.

## Contents
1. Identify the profile
2. What changes in the plan
3. Baselines without Privy history
4. Segments without engagement history
5. Imported lists and consent
6. Deliverability for a new sending setup
7. Interview additions

---

## 1. Identify the profile

| Profile | How to tell | Where last year's sales come from | Where last year's email/SMS results come from |
|---|---|---|---|
| **A. Returning** | Privy activity before Nov 2025 | Shopify | Privy (the default plugin behavior) |
| **B. Switched to Privy** | Joined Privy after Nov 2025, Shopify orders go back past Nov 2025 | Shopify | The merchant, if they want to share numbers from their previous tool. Optional |
| **C. New store** | Shopify orders start after Nov 2025, or the store didn't sell during BFCM 2025 | None | None |

Also note how long they've been on Privy, because it decides what their own recent data can support:
- **90+ days:** recent Privy data is solid enough for rates, engagement segments, and display performance.
- **30-89 days:** usable, but label rates as early reads.
- **Under 30 days:** treat Privy rates as too early to rely on; build around Shopify data and conservative assumptions.

Say it plainly in the snapshot, without making it sound like a problem: "You joined Privy in July, so I'll use your Shopify sales from last year and your Privy results since July. There's no Privy history from last BFCM, and that's fine."

## 2. What changes in the plan

For profiles B and C, shift the plan in four ways:
1. **Foundations come first.** Deliverability setup and warm-up, the consent check on imported contacts, and the Core flows go in the first phase, dated first. Most flows will show as Missing, which is expected for a new account. It is not a failing grade, so frame it as "set up for BFCM" rather than "fix."
2. **Scope is tighter.** Use the lean scope from `selection-rules.md` regardless of GMV band: Core flows and Core segments, and Conditional items only if clearly needed. Everything is net-new, so there is more to build than a returning merchant has.
3. **Cadence is lighter.** A sending reputation still being built can't absorb a full BFCM calendar. Start with the core four campaigns (teaser, early access, launch, last chance). Add the mid-sale, Cyber Monday, and extension sends only for engaged contacts, and only if warm-up is on track (section 6).
4. **Progress counts only the steps in this plan** (unchanged), so a new account isn't penalized for history it couldn't have.

## 3. Baselines without Privy history

The plan doesn't forecast revenue for anyone (see SKILL.md principles). For merchants new to Privy that matters even more, since there's less history to lean on.

**Profile B (has Shopify history):** show last year's BFCM revenue from Shopify as the baseline, exactly as for returning merchants (SH3). For email and SMS, the merchant's own numbers from their previous tool are welcome as merchant-supplied data (list size then, number of sends, revenue from email and SMS last BFCM), labeled "from your previous tool, as you reported." Do not name, cite, or compare against the previous vendor or its benchmarks. If they don't have the numbers, skip it.

**Review section:** profile B gets a BFCM 2025 review from Shopify (daily chart, facts, findings). Channel bars appear only if the merchant shares numbers from their previous tool (`channels_source: merchant`, labeled as reported). Profile C gets no review.

**Profile C (no BFCM history):** there's no BFCM baseline, and that's fine. Show normal daily revenue over the last 60-90 days as a reference point for reading results during the sale ("a normal day is about $X"), not as a prediction. Record the merchant's own goal only if they volunteer one.

**Goals for B and C:** use goals the merchant controls: early-access and SMS signups by Nov 20, Core flows live by a date, warm-up on track, spam complaints under 0.1%. Where they have 30+ days of Privy results, show those rates as a reference for what normal looks like, not as a projection.

## 4. Segments without engagement history

Engagement-based segments need send history. Substitute as follows until there are 60-90 days of Privy sends:

| Segment | Problem | Use instead |
|---|---|---|
| S05 Engaged Non-Buyers (clicked in 60 days) | Too little click history | Subscribers with 0 orders who joined in the last 90 days, or who clicked any send since joining |
| S20 Unengaged 90D+ | Can't be measured yet | For imported contacts, use engagement from the previous tool if it came over in the import. Otherwise suppress contacts with no Shopify order in 24+ months who haven't engaged with any Privy send |
| Engagement tiers for cadence | No history | Tier by Shopify recency (ordered in last 12 months vs older) plus any Privy engagement so far |
| S03/S04 Last BFCM customers | Fine for B (Shopify has the data); not applicable for C | Skip for profile C |

Order-based segments (VIPs, lapsed, repeat, category) work normally from Shopify for profile B, and they are often the strongest audiences a new Privy merchant has.

## 5. Imported lists and consent

If contacts were imported from another tool:
- **Email:** confirm the import only includes people who opted in to marketing. Leave out contacts who unsubscribed or hard-bounced in the previous tool.
- **SMS:** only send SMS to contacts whose consent is documented (source, date, and the consent language they agreed to), and keep those records. Consent is to the brand, not the tool, but it must be provable. Follow Privy's SMS import requirements and confirm with counsel.
- **New number:** if SMS now come from a different number than before, send a short intro SMS before BFCM ("It's [Brand]. This is our new number for SMS.") so the first BFCM SMS isn't from an unfamiliar sender.
- Put any unresolved import question in the plan as a P1 item with an owner.

## 6. Deliverability for a new sending setup

This is the biggest BFCM risk for a merchant new to Privy: a heavy send calendar on a sending reputation that is still being built.
- **Authentication first:** SPF, DKIM, and DMARC on the sending domain, plus one-click unsubscribe, before any large send (see `best-practices-2026.md` section 9).
- **Warm up gradually:** start with the most engaged and most recent contacts (recent buyers, recent signups, recent clickers), then widen the audience in stages over the weeks before BFCM, only while complaint and bounce rates stay low. Aim to have sent to the full BFCM audience at least once before Thanksgiving week, so the peak isn't the first time mailbox providers see that volume. Privy doesn't publish a fixed warm-up schedule, so the plan gives an audience order (which segments first, second, third), not volume numbers or daily caps. Pace depends on list size and results.
- **Time check:** if fewer than about four weeks remain and warm-up hasn't started, cut BFCM email volume: send to engaged and recent contacts only, and put the least-engaged contacts on a lighter schedule. Say this plainly in the plan; it protects revenue for all the sends that matter.
- **Monitor from the first send:** spam complaints (aim under 0.1%), bounces, and unsubscribes after every warm-up send. Pause and narrow the audience if complaints rise.

## 7. Interview additions (profiles B and C)

Ask these in place of the questions that assume last year's Privy data (for example G1):

K1. When did you start sending from Privy, and did you bring contacts over from another tool?
Options: Started fresh / Imported email only / Imported email and SMS / Not sure
K2. (If imported) Did you leave out unsubscribed and bounced contacts, and do you have consent records for SMS?
Options: Yes / Some / Not sure
K3. (Profile B) Want to share last BFCM's email/SMS results from before Privy? It gives the plan a baseline to compare against, but it's optional.
Options: Yes, I'll share / Skip
K4. Have you sent a large campaign from Privy yet?
Options: Yes, to most of the list / Only small sends / Not yet
Feeds: the deliverability deep dive in `interview-bank.md` module H (it always fires for profiles B and C when K4 is not "Yes, to most of the list").
