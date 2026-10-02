---
name: privy-brand-guidelines
description: "Design, build, or substantially improve an official Privy-authored artifact: reports, audits, proposals, benchmarks, one-pagers, calculators, decision pages, dashboards, and slide-like pages for ecommerce merchants and Privy teams. Use whenever an agent produces a visual page that should read as unmistakably Privy: spruce and lemon, Camera Plain and Matter, calm editorial hierarchy, merchant-first language, and evidence over hype."
version: 1.0.0
---

# Design artifacts like Privy

Act as a senior Privy designer, editor, and design engineer. Turn the material you are given into a page a Shopify merchant, a Privy CSM, or a Privy executive would trust on first read. Shape the argument and the interface together. Do not restyle a data dump, and do not assemble a generic SaaS template and paint it green.

The target is Privy judgment, not Privy decoration.

## Who Privy is

Privy helps ecommerce brands grow revenue with email, SMS, and on-site displays (popups, flyouts, bars, embedded forms), paired with real human expert coaching. Its customers are owner-operators and lean marketing teams, mostly on Shopify, who are busy, practical, and allergic to jargon.

Every Privy artifact should feel like advice from the smartest marketer the merchant knows: **confident, warm, plainspoken, specific, and on their side.** Confidence comes from clarity and evidence, never from hype, exclamation points, or decoration.

Brand in one line: **deep spruce set in a calm neutral field, lit by electric lemon type, with typography that does the work.**

## Priority order

When requirements compete, protect them in this order:

1. Supplied facts, numbers, units, periods, formulas, qualifiers, and privacy constraints.
2. The host project's framework, routes, components, and existing Privy tokens.
3. The reader's question, the strongest supported answer, and the evidence that earns it.
4. Unmistakable Privy authorship: logo, spruce and lemon, Camera Plain and Matter, restraint.
5. A composition specific to this material, not a template.
6. Responsive polish, interaction, and detail, without weakening hierarchy.

Ask one grouped set of questions only when guessing could change a number, a claim, a recommendation, a customer's identity, or a call to action. Otherwise omit the unknown, label it honestly, and proceed.

## Where this applies

| Surface | Use this file? | Notes |
| --- | --- | --- |
| Reports, audits, graders, benchmarks, proposals, one-pagers, calculators, internal decision docs | Yes, fully | The primary target. |
| Marketing pages in `privy-marketing-site` | Yes, with the repo's components | Use `components/ui/*`, `styles/*.css`, and `typography-*` classes instead of the standalone CSS below. |
| Privy product UI (dashboard, builders) | Tokens yes, composition no | Product chrome follows the product design system. Denser, smaller radii, light-first. |
| Merchant-authored content (a merchant's popup, email, landing page) | No | That content wears the **merchant's** brand. Privy styling is limited to surrounding editor chrome. |

---

## Work in four passes

### 1. Frame the reader's job

Before designing, privately answer:

- Who opens this, and what do they need to decide or understand?
- What is the single strongest supported answer?
- What evidence makes it credible?
- What caveat or tradeoff changes how it should be read?
- What belongs in the audit trail rather than the first read?

Support two reading speeds:

- **Skim path:** logo, title, headings, the decisive numbers, captions, and the closing action tell the whole story in under a minute.
- **Audit path:** exact tables, assumptions, methodology, and sources preserve the record for anyone who wants to check the math.

Write the skim path so a busy store owner could repeat it to a co-founder. Keep exact metric names and units in the audit path. Define any unfamiliar term in plain words the first time it appears.

Separate observation, calculation, projection, and recommendation. Never invent intent, urgency, deadlines, benchmarks, or certainty. "Your welcome flow earned 18% of email revenue last quarter" is an observation. "Adding an SMS step could lift it" is a projection and must read like one.

### 2. Choose the composition

The first viewport is the argument, not a masthead followed by setup. If the reader saw only that viewport, they should remember the central number, decision, or tool.

Name the obvious layout the category suggests (hero, then three cards, then a table), then reject it unless the material earns it. Match the opening to the job:

- **A recommendation:** the answer and its decisive basis are co-primary.
- **A grade or score:** the grade, the one-line reason, and the biggest lever sit together. Do not bury the "why" below the fold.
- **A comparison:** put alternatives on the same visual basis so the difference is seen, not reconstructed.
- **A trend or benchmark:** the relationship or the exception leads; exact records follow.
- **A calculator:** the working tool is the focal object in the first viewport.

Choose geometry before components:

- Magnitude or rank: length on a shared scale.
- Change over time: horizontal order.
- Share of a whole: proportion.
- Threshold or goal: distance from a marked boundary.
- A flow or journey (signup, welcome series, abandoned cart): sequence and connection.
- Qualitative options: aligned rows or deliberately contrasted columns.

Use tables for lookup, prose for a single conclusion, and charts only when the relationship becomes faster to see. Give every artifact one organizing move that belongs to its material and could not be transplanted into an unrelated page, such as a customer-journey spine for a lifecycle audit or a before/after revenue ladder for a migration proposal.

**Squint test:** blur your eyes; the dominant claim is obvious. **Text-mask test:** with words hidden, hierarchy still shows identity, emphasis, grouping, and progression. If every block weighs the same, redesign before coding.

### 3. Apply the visual system

Use the tokens, type roles, and primitives below. They are the design authority. Do not introduce a parallel system.

### 4. Inspect and revise privately

Render the page. Check the first viewport, the full scroll, light and dark themes, and a 375px-wide viewport. Fix the highest-impact defect, render again, repeat. Deliver the page, not a critique report. See the review checklist at the end.

---

## Visual system

### Logo and authorship

Every Privy artifact carries the Privy wordmark in the top-left of the header and a quiet footer. The wordmark is lowercase `privy` with the distinctive descending `p` and `y`. Never retype it in a font, never recolor it outside the rules below, never add effects.

- Light backgrounds: wordmark in Spruce 950 `#062B37`.
- Dark or spruce backgrounds: wordmark in Lemon 300 `#E3E32B` or Mint 50 `#F3FCF5`.
- App icon and avatar: the wordmark in Lemon 300 centered in a Spruce 950 circle. Use it only where a square mark is required.
- Minimum height 20px on screen. Clear space on every side at least the height of the `i` dot.
- Source file: `public/static/images/logo.svg` in `privy-marketing-site`. For standalone artifacts, inline this SVG. It uses `currentColor`, so set `color` on its parent:

```html
<svg class="privy-wordmark" viewBox="0 0 396 162" role="img" aria-label="Privy" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path d="M104.509 72.8897V126.939H128.164V75.2091C128.164 62.5856 135.998 54.943 147.37 54.943C152.523 54.943 156.953 56.0076 160.509 57.6046V34.8479C156.535 33.289 152.352 32.3574 144.688 32.3574C120.33 32.3574 104.509 48.7072 104.509 72.8897Z"/><path d="M184.773 0C176.767 0 170.378 4.79087 170.378 12.2624V13.5171C170.378 20.7985 176.786 25.6084 184.773 25.6084C192.759 25.6084 198.996 20.7985 198.996 13.5171V12.2624C198.996 4.79087 192.778 0 184.773 0Z"/><path d="M196.505 34.8479H172.85V126.939H196.505V34.8479Z"/><path d="M46.6077 32.4715C20.861 32.4715 0.00125518 53.0798 0.00125518 81.1027C0.00125518 81.2738 0.00125518 81.4639 0.00125518 81.635C-0.0367754 82.0913 0.799897 140.989 1.08513 160H23.2569V123.897C23.2569 122.338 25.0634 121.445 26.3184 122.395C37.1381 130.684 51.8559 132.395 64.5581 127.928C76.4617 122.529 85.8742 111.901 90.3428 98.6882C90.3618 98.6692 90.3618 98.6502 90.3618 98.6502C99.5082 63.6312 77.3364 32.4715 46.5887 32.4715H46.6077ZM46.5506 108.384C33.6963 108.384 23.2759 97.0342 23.2759 83.0418C23.2759 69.0494 33.6963 57.6996 46.5506 57.6996C59.405 57.6996 69.8444 69.0494 69.8444 83.0418C69.8444 97.0342 59.405 108.384 46.5506 108.384Z"/><path d="M272.642 34.8479L252.011 96.5209L231.74 34.8479H205.956L239.746 126.92H262.868L298.066 34.8479H272.642Z"/><path d="M370.894 34.8479L349.027 94.7529L328.224 34.8479H302.439L337.123 124.259L321.302 159.981H346.536L395.975 34.8479H370.894Z"/></svg>
```

The header's right side may hold at most two sourced fields, such as the merchant's store name, the period, or "Prepared by your Privy CSM". Use sentence case. Do not invent metadata. The footer holds the wordmark (or nothing) on the left and at most one line on the right, such as "Privy · privy.com" or a confidentiality note. Separate header and footer with space, not rules.

### Color

Privy is two colors on a neutral field: **Spruce**, a deep blue-green that carries authority and is the only brand color used for fills, and **Lemon**, an electric yellow that carries energy and is **only ever used for type and the logo on spruce or dark surfaces**. Neutrals do almost all the work.

#### Brand palette

| Token | Hex | Role |
| --- | --- | --- |
| Spruce 1000 | `#0C1C22` | Dark-theme canvas. |
| Spruce 950 | `#062B37` | Primary ink for brand moments, hero bands, primary button fill, logo on light. |
| Spruce 900 | `#254E5A` | Secondary brand fill, hover on 950, primary chart series. |
| Spruce 800 | `#2D5A5F` | Rarely used; deep chart series. |
| Spruce 700 | `#3B706F` | Brand-colored text and links on light (5.6:1 on white). |
| Spruce 600 | `#4A8584` | Chart series and icons only. Not for body text (4.2:1). |
| Spruce 500 | `#6AAF9A` | Chart series on dark; accent borders. |
| Spruce 400 | `#83D2B3` | Chart series; illustration only. |
| Mint 200 | `#BDF1D8` | Soft positive highlights, chart series on dark, selection. |
| Mint 100 | `#DEF7E9` | Faint positive wash, hover on mint. |
| Mint 50 | `#F3FCF5` | Body text on spruce bands; faint brand wash. |
| Lemon 300 | `#E3E32B` | **The accent, text only.** Headlines and hero numbers on spruce, primary button label, logo on dark. |
| Lemon 200 | `#ECEF8E` | Text only. Softer lemon for badge labels and secondary emphasis on spruce. |
| Lemon 100 | `#F7FAC2` | Text only. Small print and footer text on spruce (used in Privy emails). |

**Spruce 950 has drifted across sources:** `#062B37` (marketing site `styles/colors.css`), `#052B37` (logo SVG and transactional emails), `#052C38` (product tokens), `#053737` (product app-icon circle). They are visually identical. Use `#062B37` in new work and do not "correct" existing files for this alone.

#### Neutrals

| Token | Hex | Role |
| --- | --- | --- |
| White | `#FFFFFF` | Raised surfaces, cards, inputs. |
| Neutral 50 | `#FAFAFA` | Page canvas. |
| Neutral 100 | `#F5F5F5` | Secondary surface, table header, neutral chip. |
| Neutral 200 | `#E5E5E5` | Default border and divider. |
| Neutral 300 | `#D4D4D4` | Strong border, input border on hover. |
| Neutral 400 | `#A3A3A3` | Disabled text, gridlines on dark. |
| Neutral 500 | `#737373` | Placeholder and large metadata (4.5:1 on canvas, fragile for text). Comparison chart series. |
| Neutral 600 | `#525252` | Secondary text (7.5:1). |
| Neutral 900 | `#171717` | Headings and strong text. |
| Neutral 950 | `#0A0A0A` | Body text. |

#### Semantic state

| Token | Light | Dark | Use |
| --- | --- | --- | --- |
| Success | `#15803D` on `#F0FDF4` | `#4ADE80` | Passed checks, healthy metrics. |
| Warning | `#A16207` on `#FEFCE8` | `#FACC15` | Needs attention, at risk. |
| Error | `#B91C1C` on `#FEF2F2` | `#F87171` | Failing, broken, blocked. |
| Info | `#3B706F` on `#F3FCF5` | `#BDF1D8` | Neutral guidance. Uses the brand spruce. |

#### Color rules

- **Lemon is text, never a fill.** Never use lemon for backgrounds, buttons, badges, highlights, callouts, chart bars or areas, borders, or any filled shape. It appears only as type (and the logo) on Spruce 950, Spruce 900, or the dark canvas.
- **Lemon never appears on light surfaces.** It is 1.4:1 on white. On light pages, brand emphasis comes from Spruce, not Lemon.
- **The signature pairing is lemon type on spruce.** Lemon 300 on Spruce 950 is 10.9:1, on Spruce 900 6.6:1. That is the Privy look: a spruce band with a lemon headline, a spruce button with a lemon label.
- **Keep lemon scarce.** One lemon headline or hero number per spruce band, plus button labels. If everything is lemon, nothing is.
- **Design in neutrals first.** Add spruce for brand weight, fills, and hierarchy, lemon type for the single most important statement on a spruce surface, and semantic color only for real state. Always pair state color with a word or icon.
- Do not color a number green just because it is good. Color encodes state, not sentiment.
- **Never** use gradients, gradient text, glows, blobs, grain, glass, or colored side rails. The only allowed gradient is a labeled continuous data scale.

### Typography

Two brand typefaces. Camera Plain speaks; Matter explains.

| Family | Role | Weights |
| --- | --- | --- |
| **ABC Camera Plain** | Display, titles, section headings, big numbers | Regular 400, Medium 500 |
| **Matter** | Body, labels, controls, tables, captions. The product dashboard uses Matter for everything. | Regular 400, Medium 500, SemiBold 600 |
| Mono (fallback only) | Code, UTM strings, IDs, API keys, timestamps | 400 |

**Loading the brand fonts.** Both are licensed commercial fonts. Inside Privy repos, use the installed files (`fonts/camera-plain/*`, `fonts/display-matter/*`) via `next/font/local`, exposed as `--font-camera` and `--font-primary`. Do not upload or embed the font files in externally hosted artifacts, and do not base64 them into HTML.

**Standalone artifacts** (claude.ai artifacts, v0, static HTML) use the approved Google Fonts stand-ins, which match proportions and tone closely:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600&family=Figtree:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

```css
--privy-font-display: "ABC Camera Plain", "cameraPlain", "Hanken Grotesk", ui-sans-serif, system-ui, sans-serif;
--privy-font-body: "Matter", "displayMatter", "Figtree", ui-sans-serif, system-ui, sans-serif;
--privy-font-mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace;
```

#### Type roles

Use only these roles. Do not create arbitrary sizes or weights.

| Role | Family | Size | Weight | Line height | Tracking | Use |
| --- | --- | --- | --- | --- | --- | --- |
| Display | Display | `clamp(3rem, 6vw, 4.5rem)` | 500 | 1.0 | -0.035em | One page-defining statement or hero number. Once per page, at most. |
| Title | Display | `clamp(2rem, 4vw, 3rem)` | 500 | 1.05 | -0.025em | The page `h1`. |
| Heading L | Display | `clamp(1.5rem, 2.5vw, 1.875rem)` | 500 | 1.2 | -0.015em | Major section turns (`h2`). |
| Heading M | Display | `clamp(1.25rem, 2vw, 1.5rem)` | 500 | 1.25 | -0.01em | Subsections (`h3`). |
| Heading S | Body | `1.125rem` | 600 | 1.35 | -0.005em | Card titles, table groups (`h4`). |
| Lede | Body | `clamp(1.125rem, 1.5vw, 1.25rem)` | 400 | 1.5 | 0 | One short orienting paragraph under the title. |
| Body | Body | `1rem` | 400 | 1.6 | 0 | Reading text. Never smaller. |
| Compact | Body | `0.875rem` | 400 | 1.5 | 0 | Tables, dense lists, helper text. |
| Label | Body | `0.875rem` | 500 | 1.3 | 0 | Field labels, stat labels, button text. Never above a heading. |
| Caption | Body | `0.8125rem` | 400 | 1.45 | 0 | Chart captions, sources, footnotes. Secondary color. |
| Stat | Display | `clamp(2.25rem, 4vw, 3.5rem)` | 500 | 1.0 | -0.03em | Hero metrics. Always `tabular-nums`. |

Rules:

- **Sentence case everywhere**: headings, buttons, tabs, labels. Product names keep their capitalization (Privy, Shopify, Klaviyo, SMS).
- **No eyebrows. Ever.** No small label above a heading, in any case or color: not "Overview", not "Store health grade", not "Step 2", not a pill that restates the section. It is the most recognizable sign of AI-generated layout. If the context matters, put it in the heading ("Your store health grade is B−") or in the lede below it. A section starts with its heading.
- The only small text allowed above a large element is a **stat label** directly above its own number (label, value, detail), because it names that value rather than introducing a section.
- Headings state the claim, not the genre. "Your popups convert at twice the Shopify median" beats "Popup performance overview".
- Use `font-variant-numeric: tabular-nums` for every number that sits in a column, stat, or table.
- Keep prose at 60 to 70 characters per line (`max-width: 38rem` at body size). Rewrite before shrinking.
- Hierarchy comes from size and weight first, then space, then color. Never from boxes.
- Fix stranded single words in large headings by rewriting or adjusting the measure, not by shrinking one heading. Use `text-wrap: balance` on headings and `text-wrap: pretty` on prose.

### Space, grid, and rhythm

Base unit 4px. Use only these steps:

`4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 · 64 · 80 · 96 · 128`

- **Grid:** 12 columns desktop (max content width 1200px, 1440px for full-bleed bands), 6 on tablet, 4 on mobile. Gutters 24px desktop, 16px mobile. Side padding 16px minimum on mobile.
- Prose occupies 6 to 7 columns. Tables, charts, calculators, and comparisons may use all 12.
- **Relationships, not a uniform stack:** heading to its paragraph 12 to 16px; paragraph to paragraph 16px; label to value to detail 4 to 8px; group to group 32 to 48px; section to section 80 to 128px.
- Give every gap one owner. The parent's `gap` sets spacing; children do not add competing margins.
- Every element aligns to a shared edge, baseline, or grid line. Peers share type roles and internal rows.
- Open space must frame the focal object. A large empty rectangle from an underfilled split is a layout failure: rebalance or stack.

### Shape, surface, and depth

Privy is softer than a pure monochrome system. Generous radii and pill controls are signature, but surfaces are earned.

| Token | Value | Use |
| --- | --- | --- |
| `--privy-radius-xs` | 6px | Checkboxes, tiny chips, inline code. |
| `--privy-radius-sm` | 10px | Inputs in dense contexts, tooltips, table wrappers. |
| `--privy-radius-md` | 16px | Standard cards, callouts, chart frames. |
| `--privy-radius-lg` | 24px | Feature cards and spruce bands (the marketing-site card radius). |
| `--privy-radius-pill` | 9999px | **All buttons**, segmented controls, badges, tabs. |

- The page is one continuous `#FAFAFA` canvas. Use a white card only for a real group that spacing cannot express (a selectable option, a calculator, a recommended plan). Never nest cards.
- **Spruce band:** a full-width or large-radius Spruce 950 block with Mint 50 body text and lemon display type is Privy's signature contrast moment. Use at most two per page: typically the opening and the closing action.
- Borders are 1px Neutral 200. Prefer a hairline ring (`box-shadow: 0 0 0 1px rgb(0 0 0 / 0.06)`) over heavy borders.
- Shadows are subtle and physical. Only two:
  - `--privy-shadow-sm: 0 1px 2px rgb(0 0 0 / 0.06), 0 0 0 1px rgb(0 0 0 / 0.06)` for buttons and raised cards.
  - `--privy-shadow-md: 0 8px 24px -8px rgb(6 43 55 / 0.18), 0 0 0 1px rgb(0 0 0 / 0.06)` for popovers, menus, and dialogs.
- No ornamental shadows, no glow, no fake depth.

### Components

These mirror the production components in `privy-marketing-site/components/ui`. Match them.

**Buttons** are pills: height 40px (default) or 52px (large), padding 16px or 24px horizontal, Label type (14px, 500). Press state `transform: scale(0.98)`. Focus shows a 2px Spruce 700 ring with a 2px offset.

| Variant | Fill | Text | Hover | Use |
| --- | --- | --- | --- | --- |
| Primary | Spruce 950 | Lemon 300 | Spruce 900 | The single most important action. One per viewport. |
| Outline | White, hairline ring, `shadow-sm` | Spruce 950 | Neutral 50 | Secondary action. |
| Ghost | Transparent | Neutral 900 | Neutral 50 fill | Tertiary, toolbars. |

On a spruce band, the primary button flips to Mint 50 fill with Spruce 950 text so it stays visible; lemon remains the headline. Never make a lemon-filled button, even though older marketing pages have one.

Directional buttons may use Privy's arrow (a 16px solid arrow that nudges 4px on hover). Do not add icons to every button.

**Badges** are pills, 12px Label type, `2px 10px` padding: Spruce 900 with Lemon 200 text (brand), Mint 50 with Spruce 700 text (highlight), Neutral 100 with Neutral 900 text (neutral), semantic tones, or a Neutral 200 outline. Use badges for real state or category, never for ordinary metadata or decoration. One tone, one meaning within an artifact: if the brand badge marks "now", don't also use it for a category.

**Segmented tabs:** a pill track in Neutral 100 (or white with a hairline ring); the active tab is a Spruce 950 pill with Lemon 300 text. This is a recognizable Privy pattern; use it for switching views of the same evidence.

**Inputs:** 40px height, white fill, 1px Neutral 200 border, 10px radius, Body type. Hover border Neutral 300. Focus border Spruce 700 plus a 3px `rgb(59 112 111 / 0.2)` ring. Labels sit above in Label type; helpers below in Caption. Errors in Error red with an icon and a sentence explaining the fix.

**Stat blocks:** label (Label, secondary) above value (Stat, Neutral 950 or Lemon 300 on spruce) above detail (Caption). Peers share identical rows. Use a stat strip only for true peers; if one number is decisive, give it more scale and let the others recede.

**Tables:**

- Semantic `<table>` with `<caption>`, `<thead>`, `<tbody>`, optional `<tfoot>`.
- Span the full content width. Put the introduction above, not beside.
- Header row: Label type, secondary color, Neutral 100 background or just a 1px bottom border.
- Rows separated by 1px Neutral 200. Row height at least 44px. No zebra striping.
- Text left-aligned; numbers right-aligned with `tabular-nums`, **including their headers**.
- Body cells `vertical-align: baseline`.
- Highlight a row only when the source supports it, with a Mint 50 fill and a text label, not color alone.

**Icons:** Lucide (the product standard, `lucide-react`), default 2px stroke at 16px inline, 1.5px at 20px and above, colored `currentColor`. Never mix in another icon set. Use an icon only when it makes an action or state faster to recognize. No icons in colored tiles. No emoji as UI.

**Grades and scores:** when an artifact grades something (a store audit, a flow health check), show the grade as a Stat or Display in Camera Plain, pair it with its meaning in words ("Strong", "Needs work", "At risk"), and use semantic color only on a small indicator next to it, never on the whole card.

### Data visualization

- Charts earn their place only when a relationship is faster to see than to read.
- **Series palette, light:** `#254E5A` (Spruce 900), `#4A8584` (Spruce 600), `#83D2B3` (Spruce 400), `#BDF1D8` with a Spruce 600 outline (Mint 200), `#737373` (Neutral 500). **Dark:** `#BDF1D8`, `#6AAF9A`, `#4A8584`, `#DEF7E9`, `#737373`. Lemon is never a chart mark; on dark it may label the decisive value as text.
- Need more than five categorical series? First ask whether they should be grouped. If not, extend with the product's grouped-series order: Spruce 700 `#3C7271`, Coral `#EC6032`, Indigo `#475AD1`, Gold `#D6A400`, Jade `#00998F`, Magenta `#B33D9D`, Sky `#0081CC`, Lime `#92B200`.
- Time series match the product's reporting charts: solid 1px horizontal gridlines, no axis border or ticks, bars with a 4px radius on the end only, and the previous period as a 1px dashed Neutral 500 line.
- The decisive series gets Spruce 900 (Mint 200 on dark). Comparison and benchmark series recede to Neutral 500 (`#737373` in both themes), which clears the 3:1 minimum for graphics against the canvas. Neutral 400 does not (2.4:1 on `#FAFAFA`), so never use it for a data mark.
- Direct labels beat legends. Put the value at the end of each bar. Reserve a clean label lane.
- Zero baselines for bars. One shared scale for peer bars. Every bar track starts and ends on the same grid lines; only the fill varies.
- Gridlines 1px Neutral 200, horizontal only, or none. No chart borders or background boxes.
- Every chart has a caption stating what to notice and what it does not show, plus units, period, and population.
- Provide a table or text alternative for material chart data.
- Default to inline SVG. Do not pull chart libraries into a standalone artifact unless the data volume requires it.

### Motion

Privy is lively, not busy. Default to stillness.

- Durations: 150ms for hover and press, 200ms for state changes, 300ms for panels and dialogs.
- Easing: `cubic-bezier(0.2, 0, 0, 1)` (ease-out) for entrances and state; `cubic-bezier(0.4, 0, 0.2, 1)` for moves.
- Allowed: button press scale, arrow nudge on hover, a number counting up once when a stat first enters view, a smooth tab indicator.
- Not allowed: scroll-triggered reveals on every section, parallax, marquees, bounce, typing effects, pulsing indicators, confetti.
- Respect `prefers-reduced-motion`: remove transforms and count-ups, keep opacity changes under 150ms.

### Imagery

Use real product screenshots, real merchant logos, and real customer quotes only when supplied and relevant. Never stock photos, AI illustrations, abstract 3D shapes, or fake UI. When a product surface must be shown and no screenshot exists, draw a simplified, clearly schematic diagram in neutrals and spruce, not a fake screenshot.

### Dark theme

Artifacts support both themes via `prefers-color-scheme`, without a visible toggle. Privy dark is **spruce-dark, not gray-dark**:

| Token | Light | Dark |
| --- | --- | --- |
| Canvas | `#FAFAFA` | `#0C1C22` (Spruce 1000, matches the product's dark page) |
| Surface | `#FFFFFF` | `#122A31` |
| Surface secondary | `#F5F5F5` | `#17323A` |
| Spruce band | `#062B37` | `#062B37` with a hairline border |
| Text primary | `#0A0A0A` | `#F3FCF5` |
| Text secondary | `#525252` | `#A3BCC0` |
| Border | `#E5E5E5` | `rgb(243 252 245 / 0.12)` |
| Accent (links, focus) | `#3B706F` | `#BDF1D8` |
| Primary button, active tab | Spruce 950 fill / Lemon 300 text | Spruce 900 fill / Lemon 300 text |
| Highlighted row, callout | Mint 50 / Spruce 950 | Mint at 7% / primary text |

On dark, lemon may be used as text for headlines and key numbers anywhere, since it passes 12:1 on Spruce 1000. The logo turns Lemon 300, matching the product's dark theme.

### Print and PDF

Merchants print artifacts and save them as PDFs. Browsers drop background colors by default, which leaves lemon type invisible on white and prints a dark theme as light text on white.

- Force the light theme when printing: set `data-theme="light"` on the root in a `beforeprint` handler and remove it on `afterprint`.
- Keep brand surfaces: `print-color-adjust: exact` on spruce bands, badges, callouts, and chart marks.
- Hide chrome that does nothing on paper: navigation, view toggles, the skip link.
- Expand disclosures before printing, so collapsed detail makes it onto the page.
- Keep rows and charts whole: `break-inside: avoid` on list rows, table rows, and chart figures, `break-after: avoid` on headings. A chart split across pages can overlap its caption with the next block.
- Tables print at full width with `overflow: visible`, never clipped inside a scroll wrapper.

---

## Voice and copy

Privy sounds like an expert coach who respects the merchant's time.

- **Plain over clever.** "You're missing 1 in 3 abandoned carts" beats "Unlock hidden cart-recovery potential".
- **Specific over superlative.** Numbers, periods, and names. Never "massive", "game-changing", "supercharge", "unlock", "skyrocket", "seamless".
- **Second person, active voice.** "Your welcome flow sent 4,210 emails." Privy is "we" when it is the actor.
- **Honest about uncertainty.** "Based on 90 days of data" or "Estimated from similar Shopify stores" sits right next to the claim.
- **Encouraging, never alarmist.** Frame gaps as the next lever to pull, not as failure. Do not manufacture urgency.
- **No exclamation points** in reports. Sparingly, if ever, in marketing.
- **No em dashes.** Use a period or a comma. Write ranges with "to."
- **Say SMS, never text or texts.** "SMS subscribers," "an SMS step," "send an SMS."
- **Show SMS messages exactly as sent.** Straight quotes and apostrophes, no ellipsis character, no emoji unless intended. Curly punctuation switches an SMS to UCS-2 encoding, which cuts one message from 160 to 70 characters. Smart punctuation applies everywhere else.
- Buttons are verbs: "Book a demo", "Try Privy free", "See the fix". Never "Click here" or "Submit".

**Vocabulary.** Use Privy's terms consistently:

| Say | Not |
| --- | --- |
| displays (popups, flyouts, bars, embedded forms) | widgets, modals, overlays |
| flows (welcome, abandoned cart, browse abandonment, win-back) | automations, journeys (except in marketing headlines) |
| campaigns | blasts |
| contacts (everyone on the list), subscribers (opted in to a channel) | users, leads |
| "you" and "your store" in customer-facing pages; merchants or brands in internal and marketing copy | clients |
| Privy CSM, expert | coach, account manager |
| list growth | lead gen |
| attributed revenue, revenue per recipient, conversion rate, click rate | RPR/CVR/CTR without defining them first |
| signups | sign-ups, opt-ins (except in technical contexts) |
| texts (casual), SMS (product and technical) | messages, blasts |

When showing how a metric is calculated, follow the product's pattern: "1,204 opens ÷ 5,880 delivered emails".

---

## Standalone starter

For a standalone HTML artifact with no host project, start from this foundation. When publishing a claude.ai artifact, drop the `<!doctype>`, `<html>`, `<head>`, and `<body>` wrappers (the host adds them) and keep the `<title>`, font links, and `<style>` at the top of the file. It is complete: tokens, themes, shell, type roles, and core primitives. Page-specific CSS may add layout using these tokens only, under a `privy-x-*` namespace. Never redeclare a `--privy-*` token.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Store audit</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600&family=Figtree:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  color-scheme: light dark;
  /* Brand */
  --privy-spruce-950: #062B37; --privy-spruce-900: #254E5A; --privy-spruce-800: #2D5A5F;
  --privy-spruce-700: #3B706F; --privy-spruce-600: #4A8584;
  --privy-mint-200: #BDF1D8; --privy-mint-50: #F3FCF5;
  --privy-lemon-300: #E3E32B; --privy-lemon-200: #ECEF8E; --privy-lemon-100: #F7FAC2; /* text only, never fills */
  /* Semantic (light) */
  --privy-canvas: #FAFAFA; --privy-surface: #FFFFFF; --privy-surface-2: #F5F5F5;
  --privy-band: var(--privy-spruce-950); --privy-band-text: var(--privy-mint-50); --privy-band-accent: var(--privy-lemon-300);
  --privy-text: #0A0A0A; --privy-text-strong: #171717; --privy-text-2: #525252; --privy-text-3: #737373;
  --privy-border: #E5E5E5; --privy-border-strong: #D4D4D4; --privy-ring: rgb(0 0 0 / 0.06);
  --privy-accent: var(--privy-spruce-700); --privy-focus: var(--privy-spruce-700);
  --privy-primary-bg: var(--privy-spruce-950); --privy-primary-fg: var(--privy-lemon-300); --privy-primary-hover: var(--privy-spruce-900);
  --privy-highlight-bg: var(--privy-mint-50); --privy-highlight-fg: var(--privy-spruce-950);
  --privy-success: #15803D; --privy-success-bg: #F0FDF4;
  --privy-warning: #A16207; --privy-warning-bg: #FEFCE8;
  --privy-error: #B91C1C;   --privy-error-bg: #FEF2F2;
  --privy-chart-1: #254E5A; --privy-chart-2: #4A8584; --privy-chart-3: #83D2B3; --privy-chart-4: #BDF1D8; --privy-chart-5: #737373;
  /* Type */
  --privy-font-display: "ABC Camera Plain", "cameraPlain", "Hanken Grotesk", ui-sans-serif, system-ui, sans-serif;
  --privy-font-body: "Matter", "displayMatter", "Figtree", ui-sans-serif, system-ui, sans-serif;
  --privy-font-mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace;
  --privy-type-display: clamp(3rem, 6vw, 4.5rem);
  --privy-type-title: clamp(2rem, 4vw, 3rem);
  --privy-type-heading-l: clamp(1.5rem, 2.5vw, 1.875rem);
  --privy-type-heading-m: clamp(1.25rem, 2vw, 1.5rem);
  --privy-type-heading-s: 1.125rem;
  --privy-type-lede: clamp(1.125rem, 1.5vw, 1.25rem);
  --privy-type-body: 1rem; --privy-type-compact: 0.875rem; --privy-type-label: 0.875rem; --privy-type-caption: 0.8125rem;
  --privy-type-stat: clamp(2.25rem, 4vw, 3.5rem);
  /* Space, shape, depth, motion */
  --privy-space-1: 4px; --privy-space-2: 8px; --privy-space-3: 12px; --privy-space-4: 16px; --privy-space-5: 20px;
  --privy-space-6: 24px; --privy-space-8: 32px; --privy-space-10: 40px; --privy-space-12: 48px; --privy-space-16: 64px;
  --privy-space-20: 80px; --privy-space-24: 96px; --privy-space-32: 128px;
  --privy-radius-xs: 6px; --privy-radius-sm: 10px; --privy-radius-md: 16px; --privy-radius-lg: 24px; --privy-radius-pill: 9999px;
  --privy-shadow-sm: 0 1px 2px rgb(0 0 0 / 0.06), 0 0 0 1px rgb(0 0 0 / 0.06);
  --privy-shadow-md: 0 8px 24px -8px rgb(6 43 55 / 0.18), 0 0 0 1px rgb(0 0 0 / 0.06);
  --privy-ease: cubic-bezier(0.2, 0, 0, 1);
  --privy-content: 1200px;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --privy-canvas: #0C1C22; --privy-surface: #122A31; --privy-surface-2: #17323A;
    --privy-band: #062B37;
    --privy-text: #F3FCF5; --privy-text-strong: #FFFFFF; --privy-text-2: #A3BCC0; --privy-text-3: #7F9CA2;
    --privy-border: rgb(243 252 245 / 0.12); --privy-border-strong: rgb(243 252 245 / 0.2); --privy-ring: rgb(243 252 245 / 0.12);
    --privy-accent: var(--privy-mint-200); --privy-focus: var(--privy-mint-200);
    --privy-primary-bg: var(--privy-spruce-900); --privy-primary-fg: var(--privy-lemon-300); --privy-primary-hover: var(--privy-spruce-800);
    --privy-highlight-bg: rgb(189 241 216 / 0.07); --privy-highlight-fg: var(--privy-text);
    --privy-success: #4ADE80; --privy-success-bg: rgb(74 222 128 / 0.1);
    --privy-warning: #FACC15; --privy-warning-bg: rgb(250 204 21 / 0.1);
    --privy-error: #F87171;   --privy-error-bg: rgb(248 113 113 / 0.1);
    --privy-chart-1: #BDF1D8; --privy-chart-2: #6AAF9A; --privy-chart-3: #4A8584; --privy-chart-4: #DEF7E9; --privy-chart-5: #737373;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --privy-canvas: #0C1C22; --privy-surface: #122A31; --privy-surface-2: #17323A;
  --privy-band: #062B37;
  --privy-text: #F3FCF5; --privy-text-strong: #FFFFFF; --privy-text-2: #A3BCC0; --privy-text-3: #7F9CA2;
  --privy-border: rgb(243 252 245 / 0.12); --privy-border-strong: rgb(243 252 245 / 0.2); --privy-ring: rgb(243 252 245 / 0.12);
  --privy-accent: var(--privy-mint-200); --privy-focus: var(--privy-mint-200);
  --privy-primary-bg: var(--privy-spruce-900); --privy-primary-fg: var(--privy-lemon-300); --privy-primary-hover: var(--privy-spruce-800);
  --privy-highlight-bg: rgb(189 241 216 / 0.07); --privy-highlight-fg: var(--privy-text);
  --privy-success: #4ADE80; --privy-success-bg: rgb(74 222 128 / 0.1);
  --privy-warning: #FACC15; --privy-warning-bg: rgb(250 204 21 / 0.1);
  --privy-error: #F87171;   --privy-error-bg: rgb(248 113 113 / 0.1);
  --privy-chart-1: #BDF1D8; --privy-chart-2: #6AAF9A; --privy-chart-3: #4A8584; --privy-chart-4: #DEF7E9; --privy-chart-5: #737373;
}

*, *::before, *::after { box-sizing: border-box; }
body {
  margin: 0; background: var(--privy-canvas); color: var(--privy-text);
  font: 400 var(--privy-type-body)/1.6 var(--privy-font-body);
  -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; text-rendering: optimizeLegibility;
}
:focus-visible { outline: 2px solid var(--privy-focus); outline-offset: 2px; border-radius: 4px; }
::selection { background: var(--privy-mint-200); color: var(--privy-spruce-950); }

/* Shell */
.privy-shell { max-width: var(--privy-content); margin-inline: auto; padding-inline: clamp(16px, 4vw, 40px); overflow-wrap: break-word; }
.privy-skip { position: absolute; left: -9999px; } .privy-skip:focus { left: 16px; top: 16px; }
.privy-header { display: flex; align-items: center; justify-content: space-between; gap: var(--privy-space-4); padding-block: var(--privy-space-6) var(--privy-space-12); }
.privy-wordmark { height: 22px; width: auto; color: var(--privy-spruce-950); display: block; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .privy-wordmark { color: var(--privy-lemon-300); } }
:root[data-theme="dark"] .privy-wordmark { color: var(--privy-lemon-300); }
.privy-meta { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: var(--privy-space-1) var(--privy-space-6); font-size: var(--privy-type-caption); color: var(--privy-text-2); }
.privy-footer { display: flex; align-items: center; justify-content: space-between; gap: var(--privy-space-4); padding-block: var(--privy-space-16) var(--privy-space-10); font-size: var(--privy-type-caption); color: var(--privy-text-2); }
.privy-footer .privy-wordmark { height: 16px; color: var(--privy-text-2); }

/* Type roles */
.privy-display, .privy-title, .privy-heading-l, .privy-heading-m, .privy-stat-value {
  font-family: var(--privy-font-display); font-weight: 500; color: var(--privy-text-strong); margin: 0; text-wrap: balance;
}
.privy-display { font-size: var(--privy-type-display); line-height: 1; letter-spacing: -0.035em; }
.privy-title { font-size: var(--privy-type-title); line-height: 1.05; letter-spacing: -0.025em; }
.privy-heading-l { font-size: var(--privy-type-heading-l); line-height: 1.2; letter-spacing: -0.015em; }
.privy-heading-m { font-size: var(--privy-type-heading-m); line-height: 1.25; letter-spacing: -0.01em; }
.privy-heading-s { font: 600 var(--privy-type-heading-s)/1.35 var(--privy-font-body); letter-spacing: -0.005em; color: var(--privy-text-strong); margin: 0; }
.privy-lede { font-size: var(--privy-type-lede); line-height: 1.5; color: var(--privy-text-2); max-width: 38rem; margin: 0; text-wrap: pretty; }
.privy-prose { max-width: 38rem; } .privy-prose > * { margin: 0; } .privy-prose > * + * { margin-top: var(--privy-space-4); } .privy-prose p { text-wrap: pretty; }
.privy-label { font-size: var(--privy-type-label); font-weight: 500; line-height: 1.3; color: var(--privy-text-2); margin: 0; }
.privy-caption { font-size: var(--privy-type-caption); line-height: 1.45; color: var(--privy-text-2); margin: 0; }
.privy-mono { font-family: var(--privy-font-mono); font-size: 0.9em; }
.privy-num { font-variant-numeric: tabular-nums; }
a { color: var(--privy-accent); text-underline-position: from-font; text-underline-offset: 3px; text-decoration-thickness: from-font; text-decoration-skip-ink: auto; }

/* Layout */
.privy-section { padding-block: var(--privy-space-20); }
.privy-section + .privy-section { padding-top: 0; }
.privy-section > * + * { margin-top: var(--privy-space-8); }
.privy-stack { display: grid; gap: var(--privy-space-4); align-content: start; } .privy-stack > * { margin: 0; }
.privy-grid { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: var(--privy-space-6); }
.privy-grid > * { min-width: 0; grid-column: span 12; }
@media (min-width: 900px) {
  .privy-span-4 { grid-column: span 4; } .privy-span-5 { grid-column: span 5; } .privy-span-6 { grid-column: span 6; }
  .privy-span-7 { grid-column: span 7; } .privy-span-8 { grid-column: span 8; }
}

/* Surfaces */
.privy-card { background: var(--privy-surface); border-radius: var(--privy-radius-md); box-shadow: 0 0 0 1px var(--privy-ring); padding: var(--privy-space-6); }
.privy-band { background: var(--privy-band); color: var(--privy-band-text); border-radius: var(--privy-radius-lg); padding: clamp(32px, 6vw, 72px); box-shadow: 0 0 0 1px var(--privy-ring); }
.privy-band :is(.privy-display, .privy-title, .privy-heading-l, .privy-stat-value) { color: var(--privy-band-accent); }
.privy-band :is(.privy-lede, .privy-label, .privy-caption) { color: rgb(243 252 245 / 0.78); }
.privy-band .privy-button:not([data-variant]) { background: var(--privy-mint-50); color: var(--privy-spruce-950); }
.privy-band .privy-button:not([data-variant]):hover { background: #FFFFFF; }
.privy-callout { background: var(--privy-highlight-bg); color: var(--privy-highlight-fg); border-radius: var(--privy-radius-md); padding: var(--privy-space-5) var(--privy-space-6); }

/* Buttons */
.privy-button {
  display: inline-flex; align-items: center; justify-content: center; gap: var(--privy-space-2);
  height: 40px; padding-inline: var(--privy-space-4); border-radius: var(--privy-radius-pill); border: 0;
  font: 500 var(--privy-type-label)/1 var(--privy-font-body); text-decoration: none; white-space: nowrap; cursor: pointer;
  transition: background-color 150ms var(--privy-ease), transform 150ms var(--privy-ease), box-shadow 150ms var(--privy-ease);
  background: var(--privy-primary-bg); color: var(--privy-primary-fg); box-shadow: var(--privy-shadow-sm);
}
.privy-button:hover { background: var(--privy-primary-hover); }
.privy-button:active { transform: scale(0.98); }
.privy-button[data-variant="outline"] { background: var(--privy-surface); color: var(--privy-text-strong); }
.privy-button[data-variant="outline"]:hover { background: var(--privy-surface-2); }
.privy-button[data-variant="ghost"] { background: transparent; color: var(--privy-text-strong); box-shadow: none; }
.privy-button[data-variant="ghost"]:hover { background: var(--privy-surface-2); }
.privy-button[data-size="lg"] { height: 52px; padding-inline: var(--privy-space-6); font-size: 1rem; }

/* Badges and tabs */
.privy-badge { display: inline-flex; align-items: center; gap: 6px; border-radius: var(--privy-radius-pill); padding: 2px 10px; font: 500 0.75rem/1.5 var(--privy-font-body); background: var(--privy-surface-2); color: var(--privy-text-strong); }
.privy-badge[data-tone="brand"] { background: var(--privy-spruce-900); color: var(--privy-lemon-200); }
.privy-badge[data-tone="highlight"] { background: var(--privy-highlight-bg); color: var(--privy-accent); }
.privy-badge[data-tone="success"] { background: var(--privy-success-bg); color: var(--privy-success); }
.privy-badge[data-tone="warning"] { background: var(--privy-warning-bg); color: var(--privy-warning); }
.privy-badge[data-tone="error"] { background: var(--privy-error-bg); color: var(--privy-error); }
.privy-tabs { display: inline-flex; gap: 4px; padding: 4px; border-radius: var(--privy-radius-pill); background: var(--privy-surface); box-shadow: 0 0 0 1px var(--privy-ring); }
.privy-tabs button { height: 36px; padding-inline: var(--privy-space-4); border: 0; border-radius: var(--privy-radius-pill); background: transparent; color: var(--privy-text-strong); font: 500 var(--privy-type-label)/1 var(--privy-font-body); cursor: pointer; transition: background-color 200ms var(--privy-ease), color 200ms var(--privy-ease); }
.privy-tabs button[aria-selected="true"] { background: var(--privy-primary-bg); color: var(--privy-primary-fg); }

/* Stats */
.privy-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: var(--privy-space-8); }
.privy-stat { display: grid; gap: var(--privy-space-2); align-content: start; }
.privy-stat > * { margin: 0; }
.privy-stat-value { font-size: var(--privy-type-stat); line-height: 1; letter-spacing: -0.03em; font-variant-numeric: tabular-nums; }

/* Tables */
.privy-table-wrap { overflow-x: auto; background: var(--privy-surface); border-radius: var(--privy-radius-md); box-shadow: 0 0 0 1px var(--privy-ring); }
.privy-table { width: 100%; min-width: 36rem; border-collapse: collapse; font-size: var(--privy-type-compact); }
.privy-table caption { text-align: left; padding: var(--privy-space-5) var(--privy-space-6) var(--privy-space-2); font-size: var(--privy-type-caption); color: var(--privy-text-2); }
.privy-table th, .privy-table td { padding: var(--privy-space-3) var(--privy-space-6); text-align: left; vertical-align: baseline; border-bottom: 1px solid var(--privy-border); }
.privy-table thead th { font-weight: 500; color: var(--privy-text-2); vertical-align: bottom; }
.privy-table tbody tr:last-child > * { border-bottom: 0; }
.privy-table .privy-num, .privy-table [data-align="numeric"] { text-align: right; font-variant-numeric: tabular-nums; }
.privy-table tr[data-highlight] > * { background: var(--privy-highlight-bg); color: var(--privy-highlight-fg); }

/* Forms */
.privy-field { display: grid; gap: var(--privy-space-2); }
.privy-input { height: 40px; padding-inline: 12px; border-radius: var(--privy-radius-sm); border: 1px solid var(--privy-border); background: var(--privy-surface); color: var(--privy-text); font: 400 var(--privy-type-body)/1 var(--privy-font-body); transition: border-color 150ms var(--privy-ease), box-shadow 150ms var(--privy-ease); }
.privy-input:hover { border-color: var(--privy-border-strong); }
.privy-input:focus { outline: none; border-color: var(--privy-focus); box-shadow: 0 0 0 3px rgb(59 112 111 / 0.2); }

/* Charts */
.privy-chart { margin: 0; display: grid; gap: var(--privy-space-3); }
.privy-chart svg { width: 100%; height: auto; overflow: visible; }
.privy-chart svg text { fill: var(--privy-text-2); font: 400 12px var(--privy-font-body); }
.privy-chart .privy-gridline { stroke: var(--privy-border); stroke-width: 1; }

@media print {
  .privy-skip { display: none; }
  .privy-band, .privy-badge, .privy-callout, .privy-chart svg { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .privy-table-wrap { overflow: visible; }
  .privy-table { min-width: 0; }
  li, tr, .privy-chart { break-inside: avoid; }
  h1, h2, h3, h4 { break-after: avoid; }
}
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; } }
</style>
</head>
<body>
<a class="privy-skip" href="#main">Skip to content</a>
<div class="privy-shell">
  <header class="privy-header">
    <!-- Inline the Privy wordmark SVG from "Logo and authorship" with class="privy-wordmark" -->
    <div class="privy-meta"><span>Acme Goods</span><span>Q3 2026</span></div>
  </header>
  <main id="main">
    <!-- Composition goes here -->
  </main>
  <footer class="privy-footer">
    <!-- Wordmark at 16px -->
    <span>Prepared by Privy</span>
  </footer>
</div>
</body>
</html>
```

### Primitive API

Use these class names by their meaning. If none fits, write semantic HTML plus a page-owned `privy-x-*` class that reads only `--privy-*` tokens. Do not guess other `privy-*` names.

- **Shell:** `privy-shell`, `privy-skip`, `privy-header`, `privy-wordmark`, `privy-meta`, `privy-footer`
- **Type** (`privy-label` names a field or stat; it never introduces a heading): `privy-display`, `privy-title`, `privy-heading-l`, `privy-heading-m`, `privy-heading-s`, `privy-lede`, `privy-prose`, `privy-label`, `privy-caption`, `privy-mono`, `privy-num`
- **Layout:** `privy-section`, `privy-stack`, `privy-grid`, `privy-span-4` through `privy-span-8`
- **Surfaces:** `privy-card`, `privy-band`, `privy-callout`
- **Controls:** `privy-button` (primary by default; `data-variant="outline|ghost"`, `data-size="lg"`), `privy-tabs`, `privy-field`, `privy-input`
- **Evidence:** `privy-badge` (`data-tone="brand|highlight|success|warning|error"`), `privy-stats`, `privy-stat`, `privy-stat-value`, `privy-table-wrap`, `privy-table`, `privy-chart`, `privy-gridline`

### In Privy codebases

- **privy-marketing-site** (Next.js, Tailwind v4, shadcn): use `components/ui/button.tsx` variants (`solid` is the primary spruce pill with lemon text, plus `outline` and `ghost`; do not use the lemon-filled `secondary` variant in new work), `components/ui/badge.tsx`, the `typography-display-*`, `typography-heading-*`, and `typography-body-*` classes from `styles/typography.css`, and the `primary-*` (spruce), `secondary-*` (lemon), and `neutral-*` scales from `styles/colors.css`. Do not add the standalone CSS or a parallel token layer.
- **Privy product app** (`Privy/Privy`, Rails + React, shadcn under `.privy` scope): use `app/javascript/dashboard/components/ui/*` and the HSL tokens in `app/assets/stylesheets/dashboard/tailwind.css`. Never use the legacy `privy-components/` styled-components or their old blue/purple palette. The product is **Matter only** (variable font, no Camera Plain), 14px body, 6px radius on controls and 8px on cards, and its primary button is Spruce 900 with Lemon 200 text rather than the marketing lemon pill. Product navigation, tabs, and metric labels use Title Case; that is a product convention, not an artifact one.
- A synced Claude Design project for the dashboard exists: "Privy Dashboard UI" (see `.design-sync/NOTES.md` in the product repo). Use it for product mockups; use this file for brand artifacts.

---

## Accessibility and responsiveness

- Landmarks, a skip link, one descriptive `h1`, ordered headings, native controls, semantic tables, `figure` with `figcaption` for charts, visible focus, and text alternatives.
- WCAG AA minimum. Never rely on color alone.
- Grid and flex children get `min-width: 0`. Reflow before shrinking. The page never scrolls horizontally.
- Long strings (URLs, discount codes, UTM parameters, IDs) must wrap. Give text in flex and grid rows `overflow-wrap: anywhere`, and the row's text column `min-width: 0`.
- Wide tables scroll inside their wrapper. For one-row-per-item data (schedules, task lists), restack into a list below about 640px of container width instead: a sideways scroll on a phone has no visible cue.
- Touch targets at least 40px.
- Works at 375px wide with 16px side gutters, and in both themes, with equivalent hierarchy.

## Review checklist

Run privately before delivering. Fix, render, repeat.

1. **First read.** Is Privy authorship immediate (wordmark, spruce and lemon, type)? Would a reader who saw only the first viewport remember the key number or decision?
2. **Language.** Could a busy merchant repeat the answer after reading only headings and captions? Are terms defined? Are qualifiers intact? Are there banned words or exclamation points?
3. **Composition.** Does every section start with its heading, with no eyebrow above it? One dominant object per section? Does every section answer a new question? Any accidental empty space?
4. **Color.** Is lemon used only as text on spruce or dark, never as a fill? Is it scarce? State color paired with words?
5. **Typography.** Camera Plain for headings and stats, Matter for everything else? Consistent roles for peers? Tabular numbers? Readable measure? Sentence case?
6. **Evidence.** Shared scales, direct labels, captions with units and period, full-width tables, numeric headers right-aligned?
7. **Restraint.** Can any card, border, badge, icon, color, or paragraph be removed without losing meaning? Remove it.
8. **Themes and reflow.** Spruce-dark theme has equal hierarchy? No overflow at 375px, even with a long URL or code? Does it print cleanly in the light theme?

## Reject these defaults

- Eyebrows of any kind: small labels, kickers, overlines, pills, or numbers (01, 02) sitting above a heading.
- Centered hero then three identical feature cards.
- Any lemon fill: buttons, badges, highlights, callouts, backgrounds, chart marks. Lemon text on light surfaces.
- Gradients, glows, blobs, grain, glass, colored side rails, ornamental shadows.
- Generic "SaaS green" or teal that is not Spruce. Purple, blue, or orange accents of any kind.
- Inter, Roboto, or system fonts when the brand fonts or approved stand-ins are available.
- Cards nested in cards, borders used to fix weak hierarchy, a box around every chart.
- Repeated metric tiles when one composed relationship would be clearer.
- Badges or pills for ordinary metadata.
- Icons in colored tiles, emoji as UI, mixed icon sets.
- Tiny gray prose, arbitrary font sizes, mismatched peer values.
- Legends instead of direct labels, bars that do not share a scale, color without meaning.
- Hype words: unlock, supercharge, skyrocket, game-changing, seamless, effortless, revolutionary.
- Stock photos, AI illustrations, fake screenshots, confetti, scroll-reveal on every section.
- Process narration ("This report is organized into…").

Do not overcorrect into sterile. Privy restraint is warm: a confident spruce band with a lemon headline, generous pills and radii, and type with personality. Calm, not cold.
