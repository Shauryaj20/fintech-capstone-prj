import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# PART A: EDA & PREPROCESSING

# 1. Load Data
df = pd.read_csv("credit_applicants.csv")

# 2. Report Exact Rates
default_rate = df['default'].mean()
missing_bureau_pct = df['credit_bureau_score'].isnull().mean()

print("="*50)
print("PART A: EDA & PREPROCESSING")
print("="*50)
print(f"Exact Default Rate: {default_rate:.2%}")
print(f"Missing Bureau Score (Thin-file): {missing_bureau_pct:.2%}")

# 3. Engineer Thin-File Flag
df['is_thin_file'] = df['credit_bureau_score'].isnull().astype(int)

# 4. Train/Test Split (75/25, Stratified)
X = df.drop(columns=['applicant_id', 'default'])
y = df['default']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)

# 5. Impute Missing Bureau Scores (Fit on TRAIN only)
train_median_score = X_train['credit_bureau_score'].median()
X_train['credit_bureau_score'] = X_train['credit_bureau_score'].fillna(train_median_score)
X_test['credit_bureau_score'] = X_test['credit_bureau_score'].fillna(train_median_score)

# 6. Encode Employment Type (One-Hot Encoding)
X_train = pd.get_dummies(X_train, columns=['employment_type'], drop_first=False)
X_test = pd.get_dummies(X_test, columns=['employment_type'], drop_first=False)

# Align columns just in case a category was missing in the test split
X_train, X_test = X_train.align(X_test, join='left', axis=1, fill_value=0)

# 7. Scale Numeric Features (Fit on TRAIN only)
numeric_cols = ['age', 'monthly_income_inr', 'existing_loans_count', 
                'credit_utilization_ratio', 'upi_monthly_inflow_inr', 
                'bounced_payments_count', 'credit_bureau_score']

scaler = StandardScaler()
X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])

# PART B: CLASSIFICATION MODELS

# 1. Train Models
lr_model = LogisticRegression(random_state=42)
dt_model = DecisionTreeClassifier(random_state=42)

lr_model.fit(X_train, y_train)
dt_model.fit(X_train, y_train)

# 2. Evaluation Helper Function
def evaluate_model(model, X, y_true, model_name):
    y_pred = model.predict(X)
    y_prob = model.predict_proba(X)[:, 1]
    
    return {
        "Model": model_name,
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred),
        "Recall": recall_score(y_true, y_pred),
        "F1 Score": f1_score(y_true, y_pred),
        "ROC AUC": roc_auc_score(y_true, y_prob)
    }

lr_metrics = evaluate_model(lr_model, X_test, y_test, "Logistic Regression")
dt_metrics = evaluate_model(dt_model, X_test, y_test, "Decision Tree")

comparison_df = pd.DataFrame([lr_metrics, dt_metrics]).set_index("Model")

print("\n" + "="*50)
print("PART B: MODEL EVALUATION COMPARISON")
print("="*50)
print(comparison_df.to_string(float_format="{:.4f}".format))

print("\nConfusion Matrix (Logistic Regression):")
print(confusion_matrix(y_test, lr_model.predict(X_test)))
print("\nConfusion Matrix (Decision Tree):")
print(confusion_matrix(y_test, dt_model.predict(X_test)))

# 3. Risk-Based Pricing Table
test_results = pd.DataFrame({
    'Actual_Default': y_test,
    'Predicted_Prob': lr_model.predict_proba(X_test)[:, 1]
})

# Bucket into quartiles for 4 distinct risk tiers
test_results['Risk_Tier'] = pd.qcut(test_results['Predicted_Prob'], q=4, labels=[
    'Tier 1 (Lowest Risk)', 'Tier 2 (Low Risk)', 'Tier 3 (Medium Risk)', 'Tier 4 (Highest Risk)'
])

pricing_table = test_results.groupby('Risk_Tier', observed=False).agg(
    Applicant_Count=('Actual_Default', 'count'),
    Observed_Default_Rate=('Actual_Default', 'mean')
).reset_index()

# Assign illustrative interest rates to check monotonicity 
interest_rates = ['10% - 12%', '13% - 15%', '16% - 18%', '19% - 24%']
pricing_table['Assigned_Interest_Rate'] = interest_rates
pricing_table['Observed_Default_Rate'] = pricing_table['Observed_Default_Rate'].map("{:.2%}".format)

print("\n" + "="*50)
print("RISK-BASED PRICING TABLE (Monotonicity Check)")
print("="*50)
print(pricing_table.to_string(index=False))
print("="*50 + "\n")