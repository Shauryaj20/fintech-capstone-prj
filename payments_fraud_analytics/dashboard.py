import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Load Data
ledger = pd.read_csv('ledger.csv')
gateway = pd.read_csv('gateway_export.csv')
merchants = pd.read_csv('merchants.csv')

# Merge for category/region breakdowns
enriched_ledger = pd.merge(ledger, merchants, on='merchant_id')

# LAYER 1: HEADLINE SCORECARDS

total_gmv = ledger['amount_inr'].sum()
success_rate = (ledger['status'] == 'captured').sum() / len(ledger)
chargeback_ratio_overall = (ledger['status'] == 'chargeback').sum() / len(ledger)

# Match Rate Logic (Identical amount AND status)
merged_gw = pd.merge(ledger, gateway, on='transaction_id', suffixes=('_ld', '_gw'))
matched_exact = merged_gw[(merged_gw['amount_inr_ld'] == merged_gw['amount_inr_gw']) & 
                          (merged_gw['status_ld'] == merged_gw['status_gw'])]
match_rate = len(matched_exact) / len(ledger)

print("="*50)
print("LAYER 1: HEADLINE SCORECARDS")
print("="*50)
print(f"Total GMV: ₹{total_gmv:,.2f}")
print(f"Overall Success Rate: {success_rate:.1%}")
print(f"Reconciliation Match Rate: {match_rate:.1%}")
print(f"Chargeback Ratio: {chargeback_ratio_overall:.2%}")
print("="*50)

# LAYER 2: TRENDS (Time-series)

enriched_ledger['date'] = pd.to_datetime(enriched_ledger['transaction_time']).dt.date
daily_trends = enriched_ledger.groupby('date').agg(
    daily_gmv=('amount_inr', 'sum'),
    daily_chargebacks=('status', lambda x: (x == 'chargeback').sum())
).reset_index()

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(daily_trends['date'], daily_trends['daily_gmv'], color='blue', marker='o', label='Daily GMV (INR)')
ax1.set_xlabel('Date')
ax1.set_ylabel('GMV (INR)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
plt.xticks(rotation=45)

ax2 = ax1.twinx()
ax2.bar(daily_trends['date'], daily_trends['daily_chargebacks'], color='red', alpha=0.3, label='Chargebacks')
ax2.set_ylabel('Chargeback Count', color='red')
ax2.tick_params(axis='y', labelcolor='red')

plt.title('Layer 2: Daily GMV and Chargeback Trends')
plt.tight_layout()
plt.savefig('layer2_trends.png')
plt.close()

# LAYER 3: BREAKDOWN (Bar charts)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# By Payment Method
pay_method = enriched_ledger.groupby('payment_method')['amount_inr'].sum().sort_values()
pay_method.plot(kind='barh', ax=ax1, color='teal')
ax1.set_title('GMV by Payment Method')
ax1.set_xlabel('Total GMV (INR)')

# By Category
category = enriched_ledger.groupby('category')['amount_inr'].sum().sort_values()
category.plot(kind='barh', ax=ax2, color='orange')
ax2.set_title('GMV by Merchant Category')
ax2.set_xlabel('Total GMV (INR)')

plt.tight_layout()
plt.savefig('layer3_breakdown.png')
plt.close()

# LAYER 4: DETAILS (Top 10 Merchants Table)

merch_stats = enriched_ledger.groupby('merchant_name').agg(
    total_txns=('transaction_id', 'count'),
    cb_count=('status', lambda x: (x == 'chargeback').sum())
).reset_index()

merch_stats['cb_ratio'] = merch_stats['cb_count'] / merch_stats['total_txns']
merch_stats = merch_stats.sort_values('total_txns', ascending=False).head(10)

# Conditional Formatting logic
merch_stats['High_Risk_Flag'] = np.where(merch_stats['cb_ratio'] > 0.01, '⚠️ > 1%', 'OK')
merch_stats['cb_ratio'] = (merch_stats['cb_ratio'] * 100).map("{:.2f}%".format)
merch_stats = merch_stats.rename(columns={
    'merchant_name': 'Merchant Name', 'total_txns': 'Total Txns', 
    'cb_count': 'Chargebacks', 'cb_ratio': 'CB Ratio %', 'High_Risk_Flag': 'Risk Flag'
})

fig, ax = plt.subplots(figsize=(10, 4))
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=merch_stats.values, colLabels=merch_stats.columns, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.5)

plt.title('Layer 4: Top 10 Merchants by Volume (with Risk Flag)')
plt.tight_layout()
plt.savefig('layer4_details.png')
plt.close()

print("\nCharts generated successfully: layer2_trends.png, layer3_breakdown.png, layer4_details.png")
