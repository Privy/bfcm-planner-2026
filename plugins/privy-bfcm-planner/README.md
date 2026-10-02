# Privy BFCM Planner

Plan Black Friday and Cyber Monday with a Privy expert's playbook, built around your own store.

Ask Claude something like "help me plan Black Friday." Claude looks at your Shopify sales and your Privy displays, flows, and contacts, shows you a quick snapshot, and asks only what your data can't answer: your offer, your dates, who's doing the work. Then it builds a Privy-branded plan you can open, share, and check off.

## What's in your plan

- Where you're starting: last BFCM's results next to your Privy account today, including your total mailable and textable contacts
- Three top recommendations, each linked to its task, and your goals
- Every task dated and grouped by area, with views by week, this week, by area, or on a calendar
- Your offer, with what you keep at each tier when you've shared your margin
- Your send calendar for email and SMS, day by day
- Ideas for taking the plan further, and links to Privy's BFCM resources
- Shared progress: check off tasks, and everyone you share the plan with sees the same checklist
- Works on your phone, in light or dark mode, and prints or saves as a PDF

## What you need

- A Claude plan with code execution turned on (Settings, then Capabilities)
- A Privy account. The Privy connector comes with this plugin: the first time you use it, Claude asks you to sign in to Privy, and it only ever sees your own account
- Optional: the Shopify connector, for last year's daily sales, top products, and inventory
- Without connectors, Privy BFCM Planner still works: Claude asks for the numbers instead

## How your data is used

Privy BFCM Planner only reads your data: it never changes anything in your Shopify store or Privy account, and your plan's tasks tell you what to change yourself. It reads your store and marketing data through your own Shopify and Privy connectors, only to build your plan. It works with totals and averages and keeps customer names, emails, and phone numbers out of the plan. The included build script runs inside Claude's workspace, makes no network requests, and only reads and writes your plan files.

## Good to know

- Plans don't forecast revenue. They show last year's actual results and steps within your control.
- Daily revenue comes from Shopify when it's connected, otherwise from Privy's copy of your store orders. Email and SMS revenue comes from Privy and is shown as totals for the sale.
- Deadline and scarcity language in your send calendar is checked against your real end time.
- Compliance items (texting hours, consent, email rules) are best-practice guidance, not legal advice.
- The plan covers the run-up through the Friday after Cyber Monday. Holiday planning is separate.

## License

Proprietary. © 2026 Privy. All rights reserved. See LICENSE for the terms of use.
