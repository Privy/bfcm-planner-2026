# Privy BFCM Planner

Build your Black Friday and Cyber Monday plan from your Privy and Shopify data and a short interview. The planner reads your account (it never changes anything), asks a few questions, and publishes your plan as a shareable page: recommendations, dated tasks with a calendar view, your send calendar, and shared progress for your team.

## Before you start

1. **Connect Privy** in your assistant's connector settings. If Privy isn't listed, add it as a custom connector with this URL: `https://mcp.privy.com/mcp`
2. **Optional: connect Shopify** for last year's daily sales, top products, and inventory.
3. **In Claude, turn on code execution** (Settings → Capabilities). The planner uses it to build your plan page.

## Start with a prompt

The quickest way in: paste the prompt for your assistant from [PROMPTS.md](PROMPTS.md) into a new chat. Claude downloads the planner from this repo itself. For ChatGPT, attach [bfcm-plan-builder.zip](https://github.com/Privy/bfcm-planner-2026/raw/main/dist/bfcm-plan-builder.zip) first.

A prompt loads the planner for that one chat. To keep it for next time, install it.

## Install

**Claude (claude.ai and the Claude apps):** download [bfcm-plan-builder.skill](https://github.com/Privy/bfcm-planner-2026/raw/main/dist/bfcm-plan-builder.skill), then go to Customize → Skills → Upload a skill.

**ChatGPT:** download [bfcm-plan-builder.zip](https://github.com/Privy/bfcm-planner-2026/raw/main/dist/bfcm-plan-builder.zip) and add it under Skills in your profile menu. In ChatGPT, the planner publishes your plan as a Site.

**Claude Code:**
```
/plugin marketplace add Privy/bfcm-planner-2026
/plugin install privy-bfcm-planner@privy
```
The Claude Code plugin includes the Privy connector.

## Use it

Ask "Help me build a BFCM plan." In Claude, you can also type `/bfcm-plan-builder` (or `/bfcm-plan` in Claude Code).

## Your data

The planner only reads your data, never changes anything in Privy or Shopify, and keeps customer names, emails, and phone numbers out of your plan. [More on how your data is used](plugins/privy-bfcm-planner/README.md#how-your-data-is-used).
