# insight.py (5)
def generate_insights(metrics):
    insights = []

    # PROFIT VS REVENUE
    if metrics["profit_current"] < metrics["revenue_current"]:
        insights.append("Revenue is growing but profit margin is thin, indicating high logistics or operational costs.")

    # GROWTH STABILITY
    growth_volatility = metrics["monthly"]["growth"].std()

    if growth_volatility > 50:
        insights.append("Revenue growth is highly volatile, indicating unstable business performance.")
    else:
        insights.append("Revenue growth is relatively stable.")

    # CUSTOMER TYPE
    if metrics["repeat_rate"] > 50:
        insights.append("Business is retention-driven with strong repeat customers.")
    else:
        insights.append("Business relies heavily on new customer acquisition.")

    # CLV
    if metrics["avg_clv"] > 500:
        insights.append("Customers have high lifetime value, supporting long-term profitability.")

    # DELIVERY IMPACT
    if True in metrics["delay_vs_review"].index:
        delayed = metrics["delay_vs_review"].get(True, 0)
        ontime = metrics["delay_vs_review"].get(False, 0)

        if delayed < ontime:
            insights.append("Delayed orders significantly reduce customer satisfaction.")

    # CUSTOMER SATISFACTION
    if metrics["avg_review_score"] < 3.5:
        insights.append("Customer satisfaction is low, reflected by poor review scores.")

    elif metrics["avg_review_score"] < 4.2:
        insights.append("Customer satisfaction is moderate, indicating room for improvement.")

    else:
        insights.append("Customer satisfaction is high, indicating strong customer experience.")

    # GEO INSIGHT
    top_state = metrics["revenue_by_state"].idxmax()
    insights.append(f"Top revenue contribution comes from state {top_state}.")

    # PAYMENT BEHAVIOR
    top_payment = metrics["payment_distribution"].idxmax()
    high_spender = metrics["payment_aov"].idxmax()

    insights.append(f"{top_payment} is most used, while {high_spender} users spend the most per order.")

    return insights