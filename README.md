# Paytm FinTech Analytics & AI Platform Capstone

This repository contains an end-to-end FinTech analytics and AI platform, fulfilling the requirements for the capstone project. It is structured into three distinct business verticals, each self-contained within its own directory.

## Project Structure & Setup
Dependencies are managed at the part-level. You will find a `requirements.txt` inside both the `/payments_fraud_analytics` and `/credit_risk_lending_ml` folders. (Part 3 utilizes standard library packages and `pandas`). 

To set up the environment, navigate to the respective folder and install the requirements:

    pip install -r requirements.txt

## Part 1: Payments & Fraud Analytics (`/payments_fraud_analytics`)

### Execution:
1. `cd payments_fraud_analytics`
2. `python generate_data.py` (Generates synthetic ledger and gateway data)
3. Review `merchant_workbook.xlsx` (VLOOKUP, nested-IF categorization, pivot tables)
4. `python sql_analysis.py` (Builds SQLite schema, executes required JOINs and fraud queries)
5. `python reconcile.py` (Executes set-based Python payment reconciliation)
6. `python dashboard.py` (Generates 3 layers of matplotlib charts and prints headline scorecards)

### Design Decisions Summary:
Modeled typical Indian payment rails with appropriate MDR fee tiers (UPI at 0%, Cards at 2.5%). Used strict Julian date math for the SQL burner-account queries and string-truncation to bucket velocity-attack clusters. Opted for horizontal bar charts for categorical GMV breakdowns to ensure clean label readability.

---

## Part 2: Credit Risk & Lending ML (`/credit_risk_lending_ml`)

### Execution:
1. `cd credit_risk_lending_ml`
2. `python generate_data.py` (Generates synthetic credit applicant and transaction behavior data)
3. `python ml_pipeline.py` (Executes preprocessing, trains Logistic Regression & Decision Tree models, builds the risk-based pricing table, and runs the Isolation Forest anomaly detector)

### Design Decisions Summary:
Stratified the 75/25 train/test split to perfectly balance the 20% default rate. Engineered an `is_thin_file` binary flag to preserve new-to-credit signals, and strictly imputed missing bureau scores using only the training set median to prevent data leakage. Recommended Logistic Regression for production due to its interpretability and well-calibrated probabilities for risk-based pricing.

---

## Part 3: AI-Augmented FinTech Advisory (`/ai_advisory_blockchain`)

**Execution:** *(Note: This module operates in deterministic Mock Mode via the `MOCK_LLM=1` environment variable).*
1. `cd ai_advisory_blockchain`
2. `python advisory_agent.py` (Runs the Think/Act/Observe agent loop for portfolio allocation)
3. `python extract_disclosure.py` (Executes regex-based structured JSON extraction on SEC snippets)
4. `python debate.py` (Executes a 3-agent Bull/Bear/Synthesizer debate on PAYTECH)
5. `python dcf_calculator.py` (Computes FCFF, WACC, DCF sensitivity grid, and EV/EBITDA cross-check)

### Design Decisions Summary:
Leveraged the CAPM formula utilizing strictly Beta (ignoring analyst return) to compute expected portfolio returns, enforcing a strict 20% volatility threshold for human-in-the-loop escalation. Built the DCF model ensuring terminal growth remained safely ≥3% below the base WACC. The blockchain appendix justifies a 0% core allocation due to crypto's lack of intrinsic cash flows, while recommending strict behavioral biometric defenses against T.A.N.G. framework social engineering vectors.