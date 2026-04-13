#extract.py (1)
import pandas as pd

def load_data():
    return {
        "orders": pd.read_csv("data/olist_orders_dataset.csv"),
        "customers": pd.read_csv("data/olist_customers_dataset.csv"),
        "items": pd.read_csv("data/olist_order_items_dataset.csv"),
        "payments": pd.read_csv("data/olist_order_payments_dataset.csv"),
        "products": pd.read_csv("data/olist_products_dataset.csv"),
        "reviews": pd.read_csv("data/olist_order_reviews_dataset.csv")
    }