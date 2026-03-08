# 📊 Telco Customer Churn Analysis
**Author:** Keerthi RK | Data Analyst  
**Tools:** Python · SQL · Pandas · Matplotlib · Seaborn  
**Dataset:** IBM Telco Customer Churn — 7,032 customers

---

## 📌 Problem Statement
A telecom company is losing customers every month. The business needs to understand **who is churning, why they are churning, and what it costs** — so they can take targeted action to retain high-value customers.

---

## 📂 Project Structure
```
customer-churn-analysis/
├── data/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
├── charts/
│   ├── 01_executive_overview.png
│   ├── 02_deep_dive_eda.png
│   └── 03_revenue_impact.png
├── sql/
│   └── churn_analysis.sql
├── churn_analysis.py
├── requirements.txt
└── README.md
```

---

## 📊 Dataset Description
| Column | Description |
|---|---|
| customerID | Unique customer identifier |
| tenure | Months as a customer |
| Contract | Month-to-month / One year / Two year |
| MonthlyCharges | Monthly billing amount |
| TotalCharges | Total amount billed |
| Churn | Whether customer left (Yes/No) |
| InternetService | DSL / Fiber optic / None |
| PaymentMethod | How customer pays |

---

## 🔍 EDA Insights

### 1. Overall Churn
- **26.6%** of customers churned — 1 in 4 customers is leaving

### 2. Churn by Gender
- Male: **26.2%** | Female: **26.9%** — gender has minimal impact on churn

### 3. Churn by Contract Type
| Contract | Churn Rate |
|---|---|
| Month-to-month | **42.7%** 🔴 |
| One year | **11.3%** 🟡 |
| Two year | **2.8%** 🟢 |

### 4. Churn by Tenure
- **0–12 months: 47.7%** — nearly half of new customers leave early
- **61–72 months: 6.6%** — long-term customers are very loyal

### 5. Churn by Monthly Charges
- Customers paying **$70–90/month churn at 38%**
- Customers paying **<$30/month churn at only 8%**
- Higher charges = higher churn risk

### 6. Churn by Internet Service
- Fiber optic customers churn at **41.9%** vs DSL at **19%**
- Possible dissatisfaction with service quality at higher price points

### 7. Churn by Payment Method
- Electronic check users churn at **45.3%** — highest risk segment
- Auto-payment customers churn at only **15–17%**

---

## 📈 Dashboards

### Executive Overview
![Executive Overview](charts/01_executive_overview.png)

### Deep Dive EDA
![Deep Dive EDA](charts/02_deep_dive_eda.png)

### Revenue Impact
![Revenue Impact](charts/03_revenue_impact.png)

---

## 💡 Business Recommendations

| # | Recommendation | Expected Impact |
|---|---|---|
| 1 | Offer discounts to convert month-to-month → annual contracts | Reduce churn from 42.7% to ~11% |
| 2 | Retention campaign for customers in first 12 months | Address 47.7% early churn |
| 3 | Nudge electronic check users to auto-pay | Cut payment-related churn by ~28% |
| 4 | Review fiber optic pricing & service quality | Address 41.9% fiber churn |
| 5 | Loyalty rewards for customers crossing 24-month mark | Lock in long-term retention |

---

## 💰 Revenue Impact
- **Total monthly revenue at risk:** $139,131
- Reducing churn by just **5%** saves ~$26,000/month
- Annual savings potential: **~$3.1 Lakhs**

---

## 🛠️ How to Run
```bash
# Clone repo
git clone https://github.com/keerthirkwork-cell/customer-churn-analysis

# Install dependencies
pip install -r requirements.txt

# Run analysis
python churn_analysis.py
```

---

## 🔮 Future Scope
- Build predictive model (Logistic Regression / Random Forest) to score churn probability per customer
- Create Streamlit dashboard for real-time churn prediction
- Add RFM segmentation for customer value analysis

---

## 📬 Connect
**LinkedIn:** linkedin.com/in/keerthi-r-81bb82200  
**Email:** keerthirk.work@gmail.com  
**GitHub:** github.com/keerthirkwork-cell
