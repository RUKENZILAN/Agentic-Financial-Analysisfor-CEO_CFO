# PiSuite — AI Financial Executive Summary Dashboard

A standalone, browser-based AI-powered financial analysis engine that generates comprehensive executive summary reports from your balance sheet and income statement data. No server required — just open the HTML file in any modern browser.



\*\*Ready to automate your financial workflows? \[Purchase PiSuite Here(https://pi314.lemonsqueezy.com/checkout/buy/5b270c7f-84ea-4eb0-a55a-c0b5fe92dff3)\*\*

\---

## Features

* **Dual Language Support** — Full Turkish (TR) and English (EN) interface and report output.
* **AI Agent Fleet** — 5 specialized AI agents run in parallel for maximum speed:

  * **Analyst** — Overall financial health assessment
  * **Auditor** — Risk detection and anomaly identification
  * **Optimizer** — Cost-cutting recommendations with concrete savings categories
  * **Forecaster** — Trend projections and forward-looking insights
  * **DuPont** — DuPont ROE decomposition analysis
* **Multiple AI Providers** — Choose between cloud (OpenAI, Anthropic Claude, Google Gemini) or local (Ollama) models.
* **Rich Visualizations** — Charts, scorecards, color-coded risk flags, and markdown-formatted insights.
* **Data Import** — Paste financial data directly or upload Excel/CSV files.
* **Export Ready** — Generate printable executive reports from the dashboard.
* **Cross-Platform** — Works on macOS, Windows, and Linux. Just a single HTML file — no installation needed.

\---

## Quick Start

1. Download `PiSuite\_Dashboard-TR-EN.html`.
2. Open it in any modern browser (Chrome, Firefox, Edge, Safari).
3. Select your preferred AI engine on the onboarding screen.
4. Enter your financial data (Balance Sheet + Income Statement).
5. Click **Generate Executive Summary**.

\---

## What's New

### v1.2 (Latest)

* **Number Format Flexibility** — Data input now accepts both Turkish (`.`-thousands, `,`-decimal: e.g. `1.234,56`) and English (`,`-thousands, `.`-decimal: e.g. `1,234.56`) number formats automatically. Currency symbols and percentages are also parsed correctly.
* **Forecast Chart Fix** — Resolved an issue where the Budget Simulations \& Forecasts chart rendered empty. The forecaster agent output is now safely sanitized into numeric arrays before chart rendering, with deterministic fallback projections if needed.

### v1.1

* **English Output Fixed** — Resolved an issue where Turkish words leaked into English-mode AI agent responses. All agent prompts now enforce the correct language based on your selected UI language.
* **Cost-Cutting Clarity** — Replaced the generic Turkish placeholder word "Kalem" in cost-cutting recommendations with specific, meaningful categories: Personnel, Procurement, Logistics, IT \& Software, Marketing, Travel, Facilities, and Outsourcing.
* **Prompt Hardening** — Added instructions preventing AI agents from using generic filler words like "item" or "line" in savings recommendations.
* **Performance Verified** — Confirmed that parallel agent execution preserves calculation correctness. All core financial ratios (Altman Z, DuPont, liquidity, etc.) are computed deterministically before AI analysis begins.

\---

## System Requirements

* A modern web browser with JavaScript enabled.
* An internet connection (if using cloud AI providers).
* For local AI: Ollama running locally with a compatible model.

\---

## File Overview

|File|Description|
|-|-|
|`PiSuite\_Dashboard-TR-EN.html`|The complete standalone application. Contains all HTML, CSS, and JavaScript. No external dependencies required at runtime except CDN libraries and your chosen AI API.|

\---

## Privacy \& Security

* **Client-side only** — Your financial data never leaves your machine except via your chosen AI provider's API.
* **No telemetry** — The application does not track usage or send analytics.
* **API keys are optional** — You can use local Ollama without any cloud API keys.

