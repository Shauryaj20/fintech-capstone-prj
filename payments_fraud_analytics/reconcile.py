import pandas as pd

def reconcile_payments(ledger_df, gateway_df):
    """
    Compares an internal ledger against an external gateway export.
    Returns 4 DataFrames: missing in gateway, missing in ledger, amount mismatches, status mismatches.
    """
    # 1. Isolating the sets of transaction IDs
    ledger_ids = set(ledger_df['transaction_id'])
    gateway_ids = set(gateway_df['transaction_id'])

    # 2. Set Difference: Missing in gateway (extra in ledger)
    missing_in_gw_ids = ledger_ids - gateway_ids
    missing_in_gateway = ledger_df[ledger_df['transaction_id'].isin(missing_in_gw_ids)].copy()

    # 3. Set Difference: Missing in ledger (extra in gateway)
    missing_in_ld_ids = gateway_ids - ledger_ids
    missing_in_ledger = gateway_df[gateway_df['transaction_id'].isin(missing_in_ld_ids)].copy()

    # 4. Preparing for Mismatches using an INNER JOIN
    # We merge only the intersection of IDs to compare amounts and statuses
    merged_df = pd.merge(ledger_df, gateway_df, on='transaction_id', suffixes=('_ledger', '_gateway'))

    # 5. Amount Mismatches
    amount_mismatches = merged_df[merged_df['amount_inr_ledger'] != merged_df['amount_inr_gateway']].copy()
    # Computing the explicit difference
    amount_mismatches['amount_difference'] = amount_mismatches['amount_inr_ledger'] - amount_mismatches['amount_inr_gateway']

    # 6. Status Mismatches
    status_mismatches = merged_df[merged_df['status_ledger'] != merged_df['status_gateway']].copy()

    return missing_in_gateway, missing_in_ledger, amount_mismatches, status_mismatches


if __name__ == "__main__":
    # Loading the synthetic datasets
    ledger_data = pd.read_csv('ledger.csv')
    gateway_data = pd.read_csv('gateway_export.csv')

    # Running the reconciliation engine
    missing_gw, missing_ld, amount_miss, status_miss = reconcile_payments(ledger_data, gateway_data)

    # Reporting the discrepancy counts
    print("\n" + "="*50)
    print("PAYMENT RECONCILIATION REPORT")
    print("="*50)
    print(f"Total Ledger Rows:  {len(ledger_data)}")
    print(f"Total Gateway Rows: {len(gateway_data)}")
    print("-" * 50)
    print(f"1. Missing in Gateway (Extra in ledger): {len(missing_gw)} (Expected ~5%)")
    print(f"2. Missing in Ledger (Extra in GW): {len(missing_ld)} (Expected ~2%)")
    print(f"3. Amount Mismatches: {len(amount_miss)} (Expected ~3%)")
    print(f"4. Status Mismatches: {len(status_miss)} (Expected ~2%)")
    print("="*50 + "\n")