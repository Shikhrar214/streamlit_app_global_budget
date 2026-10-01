# streamlit_app_global_budget
# 🌍 Global Budget Analytics Dashboard

An interactive **Data Analytics & Visualization Dashboard** built with **Python, SQL, SQLite, Pandas, Plotly, and Streamlit** to analyze historical government budgets, sector-wise allocations, anomalies, correlations, and future budget trends.

🔗 **Live Demo:** https://appappglobalbudget-kejiykdtsb6eg8rmnimsuz.streamlit.app/

---

## 🚀 Project Overview

The **Global Budget Analytics Dashboard** transforms structured government budget data into an interactive analytical application.

Users can select a country and explore:

- 📈 Historical budget trends
- 🏛️ Sector-wise budget allocation
- 🚨 Budget anomalies
- 🔗 Correlation between sectors
- 🔮 Polynomial-based budget projections
- 📊 Interactive charts and analytical insights

The project demonstrates an end-to-end workflow:

**SQLite Database → SQL Queries → Python/Pandas → Data Analysis → Visualization → Streamlit Deployment**

---

## ⭐ Key Features

### 📈 1. Macro Trends

Analyze how a country's total budget changes over time.

- Year-wise budget analysis
- Interactive Plotly line charts
- Country filtering
- Historical trend identification

### 🏛️ 2. Sector Analysis

Analyze how government budgets are distributed across different sectors.

- Sector-wise allocation
- Year-wise comparison
- Interactive area charts
- Distribution analysis using box plots

### 🚨 3. Anomaly Detection

Identifies unusual budget values using statistical analysis.

- Mean and standard deviation
- Z-score calculation
- Statistical threshold-based anomaly detection
- Anomaly visualization

### 🔬 4. Research Lab

An analytical workspace for exploring relationships between sectors.

Includes:

- Sector correlation matrix
- Correlation heatmap
- Historical sector trends
- Polynomial regression
- Future budget projection

---

## 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python | Core programming & analysis |
| Pandas | Data manipulation |
| NumPy | Numerical computation |
| SQL | Data querying |
| SQLite | Relational database |
| SQLAlchemy | Database connection |
| Plotly | Interactive visualization |
| Streamlit | Web application & deployment |

---

## 🗄️ Database Design

The project uses a relational SQLite database with multiple tables:

```text
countries
    ↓
budgets
    ↓
sector_allocations
