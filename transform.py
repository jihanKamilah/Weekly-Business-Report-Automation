#transform.py (2)
import pandas as pd

def transform_data(data):
    df = data["orders"] \
        .merge(data["customers"], on="customer_id", how="left") \
        .merge(data["items"], on="order_id", how="left") \
        .merge(data["payments"], on="order_id", how="left") \
        .merge(data["products"], on="product_id", how="left") \
        .merge(data["reviews"], on="order_id", how="left")

    # datetime
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
    df["order_estimated_delivery_date"] = pd.to_datetime(df["order_estimated_delivery_date"])

    # ======================
    # 💰 REVENUE & PROFIT
    # ======================
    df["revenue"] = df["price"] + df["freight_value"]
    df["profit"] = df["price"] - df["freight_value"]  # proxy

    # ======================
    # 🚚 DELIVERY
    # ======================
    df["delay_days"] = (
        df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
    ).dt.days

    df["is_delayed"] = df["delay_days"] > 0

    df["delivery_time"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days

    # ======================
    # 👤 CUSTOMER
    # ======================
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M")

    first_order = df.groupby("customer_unique_id")["order_purchase_timestamp"].min()
    df = df.merge(first_order.rename("first_order_date"), on="customer_unique_id", how="left")

    df["is_repeat_customer"] = df["order_purchase_timestamp"] > df["first_order_date"]

    return df