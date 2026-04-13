# main.py
import pandas as pd
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage

from extract import load_data
from transform import transform_data
from simulated import simulate_data
from metrics import compute_metrics
from insight import generate_insights
from report import generate_report

STATE_FILE = "state.txt"

# ======================STATE MANAGEMENT======================
def get_run_count():
    if not os.path.exists(STATE_FILE):
        return 0
    with open(STATE_FILE, "r") as f:
        return int(f.read())

def save_run_count(count):
    with open(STATE_FILE, "w") as f:
        f.write(str(count))


def send_email(file_path, cutoff_date):

    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

    msg = EmailMessage()
    msg['Subject'] = f'[AUTO REPORT] Weekly Business Report - {cutoff_date.strftime("%d %b %Y")}'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    # BODY EMAIL
    body = f"""
Dear Team,

Please find attached the weekly business performance report for the period ending {cutoff_date.strftime("%d %B %Y")}.

This report includes key insights on revenue, profit, customer behavior, and delivery performance.

Kindly review the report for strategic evaluation and decision-making.

Thank you.

Best regards,
Jihan - Data Analyst
"""

    msg.set_content(body)

    # ATTACH FILE
    with open(file_path, 'rb') as f:
        msg.add_attachment(
            f.read(),
            maintype='application',
            subtype='pdf',
            filename=file_path
        )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("📧 Email sent!")


# ======================MAIN PIPELINE======================
def run_pipeline():

    run_count = get_run_count()

    # 🔥 SIMULATED TIME (INI SUDAH BENAR DARI KAMU)
    start_date = pd.to_datetime("2018-06-01")
    cutoff_date = start_date + pd.Timedelta(days=7 * run_count)

    print(f"\n📊 Running Weekly Report Pipeline")
    print(f"📅 Cutoff Date: {cutoff_date.date()}")
    print("-" * 50)

    # ======================
    # DATA PIPELINE
    # ======================
    data = load_data()
    df = transform_data(data)
    df_sim = simulate_data(df, cutoff_date)

    # ======================
    # METRICS & INSIGHTS
    # ======================
    metrics = compute_metrics(df_sim, cutoff_date)
    insights = generate_insights(metrics)

    # ======================
    # GENERATE REPORT
    # ======================
    filename = f"weekly_report_{cutoff_date.strftime('%Y%m%d')}.pdf"

    generate_report(metrics, insights, filename=filename)

    print(f"📄 Report generated: {filename}")

    # ======================
    # 📧 SEND EMAIL (DITAMBAHKAN DI SINI)
    # ======================
    try:
        send_email(filename, cutoff_date)
    except Exception as e:
        print("❌ Email failed:", e)

    # ======================UPDATE STATE======================
    save_run_count(run_count + 1)

    print("✅ Pipeline finished\n")


run_pipeline()
