# 📊 Weekly Business Report Automation
<img width="959" height="539" alt="Email Automated File" src="https://github.com/user-attachments/assets/3e84ea97-5e36-45a3-9db8-d4263bba6017" />

## 📌 Project Overview

This project is an **end-to-end automated data pipeline** that generates **weekly business performance reports** in PDF format and sends them via email.

The system simulates real-time data ingestion using historical data and applies a **cutoff-based approach** to mimic weekly updates. Each run advances the reporting date, allowing the pipeline to behave like a live production system.

---

## 🎯 Objectives

* Automate business reporting process
* Simulate real-time weekly data updates
* Generate actionable insights from data
* Deliver reports automatically via email
* Build a production-like data pipeline using Python

---

## 🧠 Background

In many real-world scenarios, analysts work with **historical datasets** rather than live streaming data. However, businesses require **regular reporting (weekly/monthly)** as if new data is continuously coming in.

To address this gap, this project introduces a **simulation mechanism using a cutoff date**, where:

* Data is filtered progressively based on time
* Each pipeline run represents a new reporting period
* The system behaves like a real automated reporting workflow

This approach bridges the gap between static datasets and real-world automation needs.

---

## ⚙️ Features

* 🔄 Simulated weekly data updates (cutoff system)
* 📊 Business metrics computation (Revenue, Profit, AOV, etc.)
* 📈 Data visualization (charts & trends)
* 🧾 Automated PDF report generation
* 💡 Insight generation (rule-based analytics)
* 📧 Email delivery with attachment
* ⏰ Scheduled automation using GitHub Actions

---

## 🏗️ Project Structure

```
.
├── extract.py          # Load raw datasets
├── transform.py        # Data cleaning & feature engineering
├── simulate.py         # Cutoff-based simulation
├── metrics.py          # Business metrics calculation
├── insight.py          # Insight generation logic
├── report.py           # PDF report generation
├── main.py             # Main pipeline + email automation
│
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/               # Dataset files
│
└── .github/
    └── workflows/
        └── auto-report.yml   # Automation scheduler
```

---

## 🔁 Pipeline Workflow

```
Load Data
   ↓
Transform Data
   ↓
Simulate Weekly Cutoff
   ↓
Compute Metrics
   ↓
Generate Insights
   ↓
Generate PDF Report
   ↓
Send Email
   ↓
Update State (next run)
```

---

## 📊 Key Metrics Generated

* Total Revenue (YoY comparison)
* Total Orders
* Average Order Value (AOV)
* Profit estimation
* Delay Rate & Average Delay Days
* On-Time Delivery Rate
* Customer Retention Rate
* Customer Lifetime Value (CLV)
* Payment Behavior Analysis
* Review Score Distribution

---

## 💡 Insights Generated

Examples:

* Profit margin analysis
* Revenue growth stability
* Customer acquisition vs retention
* Delivery impact on customer satisfaction
* Customer satisfaction level
* Top-performing regions
* Payment behavior patterns

---

## 📄 Report Output
<img width="323" height="372" alt="image" src="https://github.com/user-attachments/assets/09535a3d-8d34-4b53-a331-ebc0b628aa0c" />

The pipeline generates a PDF report containing:

* Executive summary
* Revenue, Profit, AOV analysis
* Product performance
* Delivery performance
* Payment behavior
* Customer experience
* Key insights

---

## 📧 Email Automation

* Automatically sends report via email
* Uses secure authentication (App Password)
* Subject dynamically includes reporting date
* Includes professional email body

---

## ⏰ Automation Schedule

The pipeline is scheduled using **GitHub Actions**:

* Runs automatically every **Monday**
* Can also be triggered manually

---

## 📦 Installation

### 1. Clone repository

```bash
git clone https://github.com/your-username/weekly-business-report-automation.git
cd weekly-business-report-automation
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### Run manually:

```bash
python main.py
```

### Run automation:

* GitHub → Actions → Run workflow

---

## 🔐 Environment Variables (Secrets)

For email automation, set the following in GitHub Secrets:

* `EMAIL_SENDER`
* `EMAIL_PASSWORD`
* `EMAIL_RECEIVER`

---

## 📊 Data Source

This project uses the Brazilian E-Commerce Public Dataset by Olist:

👉 https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

---

## 🛠️ Tech Stack

* Python
* Pandas
* Matplotlib
* ReportLab
* GitHub Actions
* SMTP (Email Automation)

---

## 🚀 Future Improvements

* Add dashboard (Streamlit / Power BI)
* Use real-time data pipeline (Airflow / Kafka)
* Improve ML-based forecasting
* Enhance visualization styling
* Add database integration (PostgreSQL)

---

## 👩‍💻 Author

**Jihan Kamilah**
-- Data Analyst | Data Enthusiast

---

## 📌 Notes

This project is designed as a **simulation of a production-level data pipeline**, showcasing skills in:

* Data engineering
* Automation
* Reporting
* Business analytics

---

## ⭐ If you find this project useful
Feel free to ⭐ the repository!
