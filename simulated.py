#simulated.py (3)
def simulate_data(df, cutoff_date):
    return df[df["order_purchase_timestamp"] <= cutoff_date].copy()