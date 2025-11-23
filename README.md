# Siddharth-Trade-Data-Analysis
Power BI dashboard built from cleaned international trade data (2017–2025) showing cost trends, supplier performance, and HSN analytics

International Trade Analytics & Dashboard (2017–2025)
📌 Project Overview

The organization subscribes to global trade data providers such as Seair and Eximpedia to monitor import/export activities across multiple countries. Historically, the analysis was performed manually in Excel, resulting in inefficiencies due to the increasing volume, complexity, and lack of automation in processing unstructured goods descriptions, unit economics, suppliers, and duty structures.
This project builds a fully scalable analytics pipeline using:
Python → text parsing, data cleaning, feature engineering
SQL → structured storage, supplier segmentation, trend analysis
Power BI/Tableau → interactive dashboards for trade, supplier, and cost analytics

🎯 Objective
To automate and modernize trade data analysis by migrating manual workflows to a scalable data pipeline, enabling the organization to:
Track macro-level import trends (YoY growth, category movement)
Analyze HSN-level Pareto concentration
Understand unit economics & landed cost
Identify active, new & churned suppliers
Detect duty anomalies and cost variations

🛠️ Tech Stack
Tool	Purpose
Python (Pandas, Regex)	Goods Description parsing, data cleaning, unit standardization
SQL (MySQL/PostgreSQL)	Aggregation queries, supplier segmentation, Pareto analysis
Power BI / Tableau	Visualization of trends, supplier insights, unit economics
Excel / CSV	Input source and intermediate storage

🔍 Key Analysis Performed:
📈 Macro Trade Trends

YoY growth for Total Value, Duty Paid, Grand Total
Category demand pattern over time
🏷 HSN Pareto & Product Category Insights
Top 25 HSN contribution to total trade
Category → Sub-category → Model drill-down

🧾 Unit Economics

Landed cost per unit calculation:
Landed Cost = Total Value (INR) + Duty Paid (INR)
USD price extraction using regex
Capacity/Model-level comparison

🚢 Supplier Lifecycle & Cost Impact

Identification of active, new, and churned suppliers
Landing cost variation by supplier
Duty anomaly detection using Z-score

📊 Dashboard Features (Power BI/Tableau):
Page	Insights
Macro Imports View	YoY growth, country/category spend trends
HSN Pareto & Categories	Category drilldown with value contribution
Supplier Analysis	Active vs. churned suppliers, cost benchmarking
Unit Economics View	Model-wise landed cost & USD price insights
Duty Analytics	Abnormal duty % detection & cost leakage

📂 Project Structure
├── data/
│   ├── raw/                # Original trade data (Excel/CSV)
│   └── processed/          # Clean & engineered dataset
├── src/
│   ├── parsing/            # Goods description text extraction (Regex/NLP)
│   ├── cleaning/           # Base cleaning & unit normalization
│   ├── feature_engineering/# Landed cost, categories, anomalies
│   └── db/                 # SQL load scripts
├── sql/                    # Analysis queries (Trend, Pareto, Supplier)
├── dashboards/             # Power BI/Tableau files
└── README.md               # Project documentation

🚀 Outcomes & Business Value

✔ Eliminates manual Excel effort
✔ Creates a repeatable & scalable trade intelligence workflow
✔ Enables faster decision-making for sourcing, negotiation & product planning
✔ Highlights cost-saving opportunities via duty anomalies and supplier benchmarking

👨‍💻 Author
Jayasurya G — Data Analytics Practitioner
