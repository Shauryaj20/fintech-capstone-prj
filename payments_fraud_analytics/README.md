# Part 1: Payments & Fraud Analytics

## Setup & Execution
1. Ensure your terminal is set to the `/payments_fraud_analytics` directory.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the data generator: `python generate_data.py` (Outputs synthetic CSVs via seed 42)
4. View the Excel artifact: Open `merchant_workbook.xlsx`
5. Run the SQL analysis: `python sql_analysis.py` (Builds SQLite DB and executes fraud queries)
6. Run the reconciliation engine: `python reconcile.py` (Outputs exact mismatch counts)
7. Run the dashboard generator: `python dashboard.py` (Prints Layer 1, generates PNGs for Layers 2-4)

## Design Decisions
* **Fee-Tier Assumptions (Excel):** Modeled typical Indian payment rails with UPI at 0.0%, Netbanking at 1.0%, Wallets at 1.5%, and Cards carrying the highest MDR at 2.5%.
* **Classification Cutoff (Excel):** Defined a "High-Value Merchant Day" as any daily transaction volume strictly greater than ₹5,000 where the region is not "East". 
* **SQL Query Logic:** For burner accounts, time windows were strictly enforced using SQLite's `julianday()` to ensure age >= 0 and < 30 days. For velocity attacks, timestamps were truncated to the nearest 10-minute string bucket (e.g., slicing to 15 characters and appending '0') to group rapid-fire clusters.
* **Chart Choices (Dashboard):** Used a dual-axis time-series for Layer 2 to correlate volume trends with fraud spikes. Horizontal bar charts were chosen for Layer 3 to cleanly display categorical revenue breakdowns without label overlap.

## Dashboard Interpretations
* **Headline Layer:** The platform processed a total GMV of ₹382,603 with a healthy overall success rate of 85.6%. However, the reconciliation match rate indicates operational friction, sitting at 90.5% due to missing records and mismatches between the ledger and gateway export. The platform-wide chargeback ratio sits at an elevated 5.12% due to targeted fraud.
* **Trends Layer:** Daily GMV remains stable across the 30-day window, showing standard day-to-day volatility. However, anomalous spikes in the daily chargeback counts (red bars) clearly emerge towards the middle and end of the month, correlating directly with the timing of the synthetic burner account and velocity attack injections.
* **Breakdown Layer:** Looking at the GMV distribution, Card and UPI methods dominate the overall volume, aligning with standard retail payment behavior. The category breakdown reveals that high-ticket segments like Travel and Grocery drive the majority of our processed INR value compared to smaller-ticket segments.
* **Details Layer:** The Top 10 Merchants table reveals severe concentrated risk. Multiple top-volume merchants triggered the conditional formatting flag (Chargeback Ratio > 1%). This indicates that the injected velocity attacks and burner accounts heavily targeted our most active merchants, requiring immediate intervention from fraud operations.