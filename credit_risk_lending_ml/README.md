# Part 2: Credit Risk & Lending ML

## Setup & Execution
1. Run `python generate_data.py` to generate the synthetic `credit_applicants.csv` and `txn_behaviour.csv`.
2. Run `python ml_pipeline.py` to execute the end-to-end classification and anomaly detection pipeline.

## Design Decisions (Part A & B)
* **Stratification:** The dataset suffers from moderate class imbalance (~20% default rate). We stratified the 75/25 train/test split on the target variable to ensure both sets contained the exact same proportion of defaulters.
* **Thin-File Handling:** To handle new-to-credit applicants safely, we engineered an `is_thin_file` binary flag to preserve the predictive signal of missing a history. We then imputed the missing bureau scores using the **training set median**. This was strictly calculated on the training split to prevent data leakage.
* **Encoding:** `employment_type` was converted using One-Hot Encoding (`pd.get_dummies`) to prevent the model from inferring false ordinal math from text categories.

## Part D: Bias-Awareness Note
Even without explicit protected attributes like gender, location, or caste in our dataset, lending models are highly susceptible to proxy bias. Features like `monthly_income_inr` can easily act as a proxy for gender due to systemic historical wage gaps, potentially leading the model to unfairly penalize female applicants. Furthermore, `employment_type` may correlate heavily with location and socioeconomic status; for instance, 'gig' workers might be geographically concentrated in specific urban zones or marginalized communities. Finally, relying strictly on `credit_bureau_score` can penalize historically underbanked demographics. While our inclusion of thin-file applicants mitigates some of this, those without formal credit histories often belong to lower-income or rural populations. If the model relies too heavily on these proxies, it risks perpetuating discriminatory lending practices.

To govern this risk before the model goes live, we must implement a maker-checker human-in-the-loop review process. Specifically, any thin-file applicant or gig worker flagged for automated decline near the decision boundary should be automatically routed to a human underwriter for manual review. Additionally, the data science team must conduct routine disparate impact audits using a secure demographic holdout set to ensure the approval rates do not disproportionately exclude protected classes.

## Final Model Comparison & Recommendation

| Metric | Logistic Regression | Decision Tree |
| :--- | :--- | :--- |
| **Accuracy** | 76.00% | 67.00% |
| **Precision** | 38.89% | 24.00% |
| **Recall** | 35.00% | 30.00% |
| **F1 Score** | 36.84% | 26.67% |
| **ROC AUC** | 71.88% | 53.12% |
| **Isolation Forest Recall** | 73.33% (11/15 seeded anomalies found) | N/A |

**Deployment Recommendation:**
I recommend deploying the **Logistic Regression** model for the Paytm Postpaid underwriting engine. While Decision Trees can capture complex non-linear patterns, they are highly prone to overfitting on tabular credit data, leading to brittle and erratic predictions in production. Logistic Regression provides critical interpretability, allowing the risk team to explain exactly why an applicant was declined (e.g., extracting the exact penalty weight for bounced payments). Furthermore, Logistic Regression provides exceptionally well-calibrated probabilities, which are absolutely essential for accurately bucketing users into the Risk-Based Pricing tiers.