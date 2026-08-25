# Part 3: AI-Augmented FinTech Advisory & Blockchain Risk

## LLM Configuration
All scripts in this module were executed using the graded baseline **Mock Mode** (`MOCK_LLM=1` or unset). No external API calls or network requests were made, and all outputs are entirely deterministic based on the provided seed data and rule-based logic.

## 1. Advisory Agent Transcripts
*   **Conservative Profile (INV01):** Agent computed an Expected Return of 9.20% and Volatility (Std Dev) of 8.44%. Result: `[APPROVED] For Conservative investor INV01, we recommend an allocation across ['PAYBOND', 'PAYGOLD', 'PAYRETAIL'] with an expected portfolio return of 9.2% and volatility of 8.4%.`
*   **Moderate Profiles (INV02, INV04):** Agent computed an Expected Return of 11.30% and Volatility (Std Dev) of 12.57%. Result: `[APPROVED]` (Volatility within safe limits).
*   **Aggressive Profiles (INV03, INV05):** Agent computed an Expected Return of 15.00% and Volatility (Std Dev) of 20.58%. Result: `[ESCALATED_TO_HUMAN_ADVISOR]` (Volatility exceeds 20% limit).

## 2. Structured Extraction Highlights
*   **doc_01:** `{"risk_flags": [], "hedging_detected": true, "sentiment": "cautious"}` *(Triggered by "assuming")*
*   **doc_02:** `{"risk_flags": ["litigation"], "hedging_detected": false, "sentiment": "neutral"}` *(Triggered by "litigation")*
*   **doc_05:** `{"risk_flags": [], "hedging_detected": false, "sentiment": "confident"}` *(Triggered by "confident" and "approved")*

## 3. Debate Demo Transcript (PAYTECH)
*   **BULL AGENT:** With an analyst expected return of 19.0% against a beta of 1.55, PAYTECH offers attractive risk-adjusted upside. This is a strong opportunity for capital appreciation.
*   **BEAR AGENT:** The risk profile is simply too aggressive. PAYTECH carries a substantial standard deviation of 34.0%, exposing investors to severe drawdowns if macroeconomic conditions deteriorate.
*   **SYNTHESIZER:** The debate highlights a classic high-risk, high-reward tradeoff for PAYTECH. While the bull correctly identifies the lucrative 19.0% expected return, the bear's concern regarding the 34.0% volatility is highly relevant. Investors must carefully weigh their individual risk tolerance against this beta of 1.55 before allocating capital.

## 4. DCF Valuation & Sensitivity Analysis
**Base Assumptions:**
*   Computed WACC: **11.55%** (Cost of Equity 13.6% via CAPM, Cost of Debt 9% pre-tax / 6.75% post-tax, 70/30 Equity/Debt split).
*   Terminal Growth Rate: **5.00%** (Maintains a safe >3% spread below base WACC).
*   Base Enterprise Value: **₹6,966,108.20**

**Sensitivity Table (WACC vs. Terminal Growth):**
| | TG 4.0% | TG 5.0% | TG 6.0% |
| :--- | :--- | :--- | :--- |
| **WACC 10.55%** | ₹7,203,476 | ₹8,260,307 | ₹9,782,192 |
| **WACC 11.55%** | ₹6,216,897 | ₹6,966,108 | ₹7,985,549 |
| **WACC 12.54%** | ₹5,462,224 | ₹6,015,953 | ₹6,738,889 |

*Worst-case cell spread (WACC 10.55% minus TG 6.0%) is 4.55%, satisfying the required safety check constraint.*