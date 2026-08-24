import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

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

print(f"Imputed missing bureau scores using training median: {train_median_score}")

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

print("Preprocessing complete. Data is ready for modeling.")
print("="*50 + "\n")