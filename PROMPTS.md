# Start the Privy BFCM Planner with a prompt

Connect Privy first (and Shopify, if you use it). See "Before you start" in the README. Then paste the prompt for your assistant into a new chat.

## Claude

Turn on code execution (Settings → Capabilities), then paste:

```
Use the Privy BFCM Planner to build my Black Friday and Cyber Monday plan.

1. Download https://github.com/Privy/bfcm-planner-2026/archive/refs/heads/main.zip into your workspace and unzip it. If the download is blocked, fetch the files from https://github.com/Privy/bfcm-planner-2026 instead.
2. Open plugins/privy-bfcm-planner/skills/bfcm-plan-builder/SKILL.md and follow it exactly, reading its reference files when it says to. Run its build script from that folder.
3. Read my data through my Privy connector, and Shopify if it's connected.
4. Publish the finished plan as an artifact.

Start now.
```

## ChatGPT

Download [bfcm-plan-builder.zip](https://github.com/Privy/bfcm-planner-2026/raw/main/dist/bfcm-plan-builder.zip), attach it to a new chat, then paste:

```
Use the Privy BFCM Planner in the attached zip to build my Black Friday and Cyber Monday plan.

1. Unzip it and open bfcm-plan-builder/SKILL.md. Follow it exactly, reading its reference files when it says to, and run its build script from that folder.
2. Read my data through my Privy connector, and Shopify if it's connected.
3. Publish the finished plan as a ChatGPT Site.

Start now.
```
