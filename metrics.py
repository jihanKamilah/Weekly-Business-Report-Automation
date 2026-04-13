#metrics.py (4)
import pandas as pd

def compute_metrics(df, cutoff_date):
    metrics = {}

    df = df[df["order_purchase_timestamp"] <= cutoff_date].copy()

    current_year = cutoff_date.year
    prev_year = current_year - 1

    df["year"] = df["order_purchase_timestamp"].dt.year

    df_current = df[df["year"] == current_year]
    df_prev = df[df["year"] == prev_year]

    #======================BASIC======================
    metrics["revenue_current"] = df_current["revenue"].sum()
    metrics["revenue_prev"] = df_prev["revenue"].sum()

    metrics["orders_current"] = df_current["order_id"].nunique()
    metrics["orders_prev"] = df_prev["order_id"].nunique()

    metrics["aov_current"] = (
        metrics["revenue_current"] / metrics["orders_current"]
        if metrics["orders_current"] > 0 else 0
    )

    metrics["aov_prev"] = (
        metrics["revenue_prev"] / metrics["orders_prev"]
        if metrics["orders_prev"] > 0 else 0
    )

    #======================PROFIT======================
    metrics["profit_current"] = df_current["profit"].sum()
    metrics["profit_prev"] = df_prev["profit"].sum()

    #======================MONTHLY TREND======================
    df["month"] = df["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()

    monthly = df.groupby("month").agg({
        "revenue": "sum",
        "profit": "sum",
        "order_id": "nunique"
    })

    monthly["aov"] = monthly["revenue"] / monthly["order_id"]
    monthly["growth"] = monthly["revenue"].pct_change() * 100
    monthly["moving_avg"] = monthly["revenue"].rolling(3).mean()

    # ensure no future leakage
    monthly = monthly[monthly.index <= cutoff_date]

    metrics["monthly"] = monthly
    metrics["monthly_revenue"] = monthly["revenue"]

    # ======================CUSTOMER======================
    metrics["repeat_rate"] = (
        df_current["is_repeat_customer"].mean() * 100
        if len(df_current) > 0 else 0
    )

    clv = df.groupby("customer_unique_id")["revenue"].sum()
    metrics["avg_clv"] = clv.mean()

    # ======================COHORT======================
    df["cohort"] = df["first_order_date"].dt.to_period("M")
    df["cohort_index"] = (
        (df["order_month"] - df["cohort"]).apply(lambda x: x.n)
    )

    cohort = df.groupby(["cohort", "cohort_index"])["customer_unique_id"].nunique().unstack()

    if not cohort.empty:
        cohort_size = cohort.iloc[:, 0]
        retention = cohort.divide(cohort_size, axis=0)
    else:
        retention = pd.DataFrame()

    metrics["cohort_retention"] = retention

    # ======================DELIVERY======================
    metrics["delay_rate"] = (
        df_current["is_delayed"].mean() * 100
        if len(df_current) > 0 else 0
    )

    metrics["avg_delay_days"] = df_current["delay_days"].mean()
    metrics["avg_delivery_time"] = df_current["delivery_time"].mean()

    metrics["on_time_rate"] = (
        (df_current["delay_days"] <= 0).mean() * 100
        if len(df_current) > 0 else 0
    )

    metrics["delay_by_state"] = (
        df_current.groupby("customer_state")["is_delayed"].mean() * 100
    )

    # ======================PRODUCT DELAY======================
    product_delay = (
        df_current.groupby("product_category_name")["is_delayed"].mean() * 100
    )

    metrics["product_delay"] = product_delay
    metrics["delay_by_product"] = product_delay  # alias for report

    # ======================CANCELLATION======================
    cancelled = df[df["order_status"] == "canceled"]

    metrics["cancellation_rate"] = (
        len(cancelled) / len(df) * 100
        if len(df) > 0 else 0
    )

    # ======================DELAY VS REVIEW======================
    metrics["delay_vs_review"] = (
        df_current.groupby("is_delayed")["review_score"].mean()
    )

    # ======================GEO======================
    metrics["revenue_by_state"] = (
        df_current.groupby("customer_state")["revenue"].sum()
    )

    # ======================PRODUCT======================
    metrics["top_products"] = (
        df_current.groupby("product_category_name")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    # ======================PAYMENT======================
    metrics["payment_distribution"] = (
        df_current["payment_type"].value_counts(normalize=True) * 100
    )

    metrics["payment_aov"] = (
        df_current.groupby("payment_type")["revenue"].mean()
    )

    # ======================REVIEW======================
    metrics["avg_review_score"] = df_current["review_score"].mean()
    metrics["review_distribution"] = (
        df_current["review_score"].value_counts().sort_index()
    )

    # ======================YOY======================
    cutoff_month = cutoff_date.month

    rev_current = df[
        (df["year"] == current_year) &
        (df["order_purchase_timestamp"].dt.month == cutoff_month)
    ]["revenue"].sum()

    rev_prev = df[
        (df["year"] == prev_year) &
        (df["order_purchase_timestamp"].dt.month == cutoff_month)
    ]["revenue"].sum()

    metrics["yoy_growth"] = (
        ((rev_current - rev_prev) / rev_prev * 100)
        if rev_prev != 0 else None
    )

    metrics["cutoff_date"] = cutoff_date

    return metrics