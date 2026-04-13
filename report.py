#report.py (6)
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

import matplotlib.ticker as mticker


# ======================HELPER TABLE======================
def build_comparison_table(monthly_df, value_col):

    monthly_df["year"] = monthly_df["month"].dt.year
    monthly_df["month_num"] = monthly_df["month"].dt.month

    pivot = monthly_df.pivot(
        index="month_num",
        columns="year",
        values=value_col
    ).sort_index()

    if 2017 in pivot.columns and 2018 in pivot.columns:
        pivot["growth"] = ((pivot[2018] - pivot[2017]) / pivot[2017]) * 100
    else:
        pivot["growth"] = None

    table_data = [["Month", "2017", "2018", "Growth (%)"]]

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    for i in pivot.index:
        table_data.append([
            months[i-1],
            f"{pivot.at[i, 2017]:,.0f}" if 2017 in pivot.columns else "-",
            f"{pivot.at[i, 2018]:,.0f}" if 2018 in pivot.columns else "-",
            f"{pivot.at[i, 'growth']:.2f}%" if pd.notnull(pivot.at[i, "growth"]) else "-"
        ])

    return table_data


# ======================CREATE CHARTS======================
def create_charts(metrics):

    monthly = metrics["monthly"].reset_index()
    monthly.columns = ["month", "revenue", "profit", "order_id", "aov", "growth", "moving_avg"]

    monthly["year"] = monthly["month"].dt.year
    monthly["month_num"] = monthly["month"].dt.month

    monthly = monthly[monthly["year"].isin([2017, 2018])]

    # REVENUE
    pivot = monthly.pivot(index="month_num", columns="year", values="revenue").dropna(how='all')
    plt.figure(); pivot.plot(marker='o')
    plt.title("Monthly Revenue Comparison (2017 vs 2018)")
    plt.xticks(range(1,13))
    plt.tight_layout()
    plt.savefig("revenue_chart.png")
    plt.close()

    # PROFIT
    pivot = monthly.pivot(index="month_num", columns="year", values="profit").dropna(how='all')
    plt.figure(); pivot.plot(marker='o')
    plt.title("Monthly Profit Comparison (2017 vs 2018)")
    plt.xticks(range(1,13))
    plt.tight_layout()
    plt.savefig("profit_chart.png")
    plt.close()

    # AOV
    pivot = monthly.pivot(index="month_num", columns="year", values="aov").dropna(how='all')
    plt.figure(); pivot.plot(marker='o')
    plt.title("Monthly AOV Comparison (2017 vs 2018)")
    plt.xticks(range(1,13))
    plt.tight_layout()
    plt.savefig("aov_chart.png")
    plt.close()

    # DELAY
    plt.figure()
    metrics["delay_by_state"].sort_values(ascending=False).head(5).plot(kind='bar')
    plt.title("Top 5 States by Delay Rate")
    plt.tight_layout()
    plt.savefig("delay_state_chart.png")
    plt.close()

    # PAYMENT
    plt.figure()
    metrics["payment_distribution"].plot(kind='pie', autopct='%1.1f%%')
    plt.title("Payment Distribution")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("payment_chart.png")
    plt.close()

    # REVIEW
    plt.figure()
    metrics["review_distribution"].sort_index().plot(kind='bar')
    plt.title("Review Score Distribution")
    plt.tight_layout()
    plt.savefig("review_chart.png")
    plt.close()


# ======================GENERATE REPORT======================
def generate_report(metrics, insights, filename=None):

    create_charts(metrics)

    styles = getSampleStyleSheet()
    content = []

    cutoff = metrics["cutoff_date"]

    if filename is None:
        filename = f"weekly_report_{cutoff.strftime('%d %b %Y')}.pdf"

    doc = SimpleDocTemplate(filename)

    # HEADER
    content.append(Paragraph("Automated Business Performance Report", styles['Title']))
    content.append(Spacer(1, 8))
    content.append(Paragraph(f"Weekly Report (Week Ending {cutoff.strftime('%d %b %Y')})", styles['Normal']))
    content.append(Spacer(1, 15))

    # EXEC SUMMARY
    content.append(Paragraph("Executive Summary", styles['Heading2']))

    table_data = [
        ["Metric", str(cutoff.year - 1), str(cutoff.year)],
        ["Total Revenue", f"{metrics['revenue_prev']:,.0f}", f"{metrics['revenue_current']:,.0f}"],
        ["Total Orders", f"{metrics['orders_prev']:,}", f"{metrics['orders_current']:,}"],
        ["AOV", f"{metrics['aov_prev']:,.0f}", f"{metrics['aov_current']:,.0f}"],
        ["Delay Rate (%)", "-", f"{metrics['delay_rate']:.2f}%"],
        ["Avg Delay Days", "-", f"{metrics['avg_delay_days']:.2f}"],
        ["On-Time Rate (%)", "-", f"{metrics['on_time_rate']:.2f}%"],
        ["Avg Review Score", "-", f"{metrics['avg_review_score']:.2f}"],
    ]

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ]))

    content.append(table)
    content.append(Spacer(1, 20))

    # ======================REVENUE======================
    content.append(Paragraph("Revenue Analysis", styles['Heading2']))
    content.append(Image("revenue_chart.png", width=450, height=220))

    monthly_df = metrics["monthly"].reset_index()
    revenue_table = Table(build_comparison_table(monthly_df.copy(), "revenue"))
    revenue_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.black),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    content.append(revenue_table)
    content.append(Spacer(1, 20))

    # ======================PROFIT======================
    content.append(Paragraph("Profit Analysis", styles['Heading2']))
    content.append(Image("profit_chart.png", width=450, height=220))

    profit_table = Table(build_comparison_table(monthly_df.copy(), "profit"))
    profit_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.black),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    content.append(profit_table)
    content.append(Spacer(1, 20))

    content.append(Spacer(1, 20))
    content.append(Spacer(1, 20))
    content.append(Spacer(1, 20))

    # ======================AOV======================
    content.append(Paragraph("AOV Analysis", styles['Heading2']))
    content.append(Image("aov_chart.png", width=450, height=220))

    aov_table = Table(build_comparison_table(monthly_df.copy(), "aov"))
    aov_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.black),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    content.append(aov_table)
    content.append(Spacer(1, 20))

    # ======================PRODUCT======================
    content.append(Paragraph("Top Product Categories (Current Year)", styles['Heading2']))

    product_data = [["Category", "Revenue"]]
    for idx, val in metrics["top_products"].items():
        product_data.append([str(idx), f"{val:,.0f}"])

    product_table = Table(product_data)
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.black),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    content.append(product_table)
    content.append(Spacer(1, 20))

    # ======================DELAY======================
    content.append(Paragraph("Delivery Performance", styles['Heading2']))

    content.append(Image("delay_state_chart.png", width=450, height=220))

    content.append(Paragraph(
        f"Delay Rate: {metrics['delay_rate']:.2f}% | "
        f"Avg Delay: {metrics['avg_delay_days']:.2f} days",
        styles['Normal']
    ))
    content.append(Spacer(1, 10))

    delay_data = [["Product Category", "Delay %"]]
    for idx, val in metrics["delay_by_product"].sort_values(ascending=False).head(5).items():
        delay_data.append([str(idx), f"{val:.2f}%"])

    delay_table = Table(delay_data)
    delay_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.black),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    content.append(delay_table)
    content.append(Spacer(1, 20))

    content.append(Spacer(1, 20))
    content.append(Spacer(1, 20))
    content.append(Spacer(1, 20))
    content.append(Spacer(1, 20))
    content.append(Spacer(1, 20))
    content.append(Spacer(1, 20))
    content.append(Spacer(1, 20))
    content.append(Spacer(1, 20))
    content.append(Spacer(1, 20))


    content.append(Paragraph("Payment Behavior", styles['Heading2']))
    content.append(Image("payment_chart.png", width=300, height=200))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Customer Experience", styles['Heading2']))
    content.append(Image("review_chart.png", width=400, height=220))

    content.append(Spacer(1, 10))
    content.append(Paragraph(f"Average Review Score: {metrics['avg_review_score']:.2f}", styles['Normal']))

    content.append(Spacer(1, 20))

    content.append(Paragraph("Key Insights", styles['Heading2']))
    for insight in insights:
        content.append(Paragraph(f"- {insight}", styles['Normal']))

    doc.build(content)