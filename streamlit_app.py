
from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, inspect
import plotly.express as px
import plotly.graph_objects as go


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Global Budget Analytics Core",
    layout="wide"
)


# --------------------------------------------------
# Database Configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "global_budget_db.db"


@st.cache_resource
def get_engine():
    return create_engine(
        f"sqlite:///{DB_PATH}"
    )


# --------------------------------------------------
# Database Validation
# --------------------------------------------------

if not DB_PATH.exists():

    st.error(
        f"Database file not found:\n\n{DB_PATH}"
    )

    st.stop()


engine = get_engine()

inspector = inspect(engine)

required_tables = [
    "countries",
    "budgets",
    "sector_allocations"
]

existing_tables = inspector.get_table_names()

missing_tables = [
    table
    for table in required_tables
    if table not in existing_tables
]


if missing_tables:

    st.error(
        "Required database tables are missing."
    )

    st.write(
        "Missing tables:",
        missing_tables
    )

    st.write(
        "Available tables:",
        existing_tables
    )

    st.stop()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title(
    "🏛️ Global Government Budget Analytics Core"
)

st.markdown(
    """
    Interactive platform exploring public finance trends,
    sector allocation, anomaly detection,
    correlation analysis and future projections.
    """
)


# --------------------------------------------------
# Countries
# --------------------------------------------------

countries = pd.read_sql_query(
    """
    SELECT country_name
    FROM countries
    ORDER BY country_name
    """,
    engine
)


if countries.empty:

    st.warning(
        "No countries found in the database."
    )

    st.stop()


selected_country = st.sidebar.selectbox(
    "Select Country",
    countries["country_name"].tolist()
)


# --------------------------------------------------
# Tabs
# --------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Macro Trends",
        "🧱 Sector Analysis",
        "🔍 Anomalies",
        "🔬 Research Lab"
    ]
)


# ==================================================
# TAB 1 — MACRO TRENDS
# ==================================================

with tab1:

    q = """
    SELECT
        b.year,
        b.Total_Budget_Billions_USD
    FROM budgets b
    JOIN countries c
        ON b.country_id = c.country_id
    WHERE c.country_name = :country_name
    ORDER BY b.year
    """

    df_macro = pd.read_sql_query(
        q,
        engine,
        params={
            "country_name": selected_country
        }
    )


    if df_macro.empty:

        st.warning(
            "No budget data found for this country."
        )

    else:

        fig = px.line(
            df_macro,
            x="year",
            y="Total_Budget_Billions_USD",
            template="plotly_dark",
            markers=True,
            title=f"{selected_country} Budget Trend"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )


# ==================================================
# TAB 2 — SECTOR ANALYSIS
# ==================================================

with tab2:

    q = """
    SELECT
        b.year,
        sa.sector_name,
        sa.allocated_percentage
    FROM sector_allocations sa
    JOIN budgets b
        ON sa.budget_id = b.budget_id
    JOIN countries c
        ON b.country_id = c.country_id
    WHERE c.country_name = :country_name
    ORDER BY b.year
    """

    df_sector = pd.read_sql_query(
        q,
        engine,
        params={
            "country_name": selected_country
        }
    )


    if df_sector.empty:

        st.warning(
            "No sector allocation data found."
        )

    else:

        c1, c2 = st.columns(2)


        with c1:

            fig = px.area(
                df_sector,
                x="year",
                y="allocated_percentage",
                color="sector_name",
                template="plotly_dark",
                title="Sector Allocation Over Time"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )


        with c2:

            fig = px.box(
                df_sector,
                x="sector_name",
                y="allocated_percentage",
                color="sector_name",
                template="plotly_dark",
                title="Sector Allocation Distribution"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )


# ==================================================
# TAB 3 — ANOMALY DETECTION
# ==================================================

with tab3:

    if df_macro.empty:

        st.warning(
            "No budget data available for anomaly detection."
        )

    else:

        mean = df_macro[
            "Total_Budget_Billions_USD"
        ].mean()

        std = df_macro[
            "Total_Budget_Billions_USD"
        ].std()


        if pd.isna(std) or std == 0:

            st.success(
                "No statistical anomalies detected."
            )

        else:

            df_macro["z_score"] = (
                df_macro[
                    "Total_Budget_Billions_USD"
                ] - mean
            ) / std


            outliers = df_macro[
                df_macro["z_score"].abs() > 1.96
            ]


            st.subheader(
                "Statistical Anomalies"
            )


            if outliers.empty:

                st.success(
                    "No significant anomalies detected."
                )

            else:

                st.dataframe(
                    outliers,
                    width="stretch"
                )


# ==================================================
# TAB 4 — RESEARCH LAB
# ==================================================

with tab4:

    q = """
    SELECT
        b.year,
        sa.sector_name,
        sa.allocated_percentage
    FROM sector_allocations sa
    JOIN budgets b
        ON sa.budget_id = b.budget_id
    JOIN countries c
        ON b.country_id = c.country_id
    WHERE c.country_name = :country_name
    """

    corr_df = pd.read_sql_query(
        q,
        engine,
        params={
            "country_name": selected_country
        }
    )


    # --------------------------------------------------
    # Sector Correlation
    # --------------------------------------------------

    if not corr_df.empty:

        st.subheader(
            "Sector Correlation Analysis"
        )


        pivot = corr_df.pivot_table(
            index="year",
            columns="sector_name",
            values="allocated_percentage",
            aggfunc="mean"
        )


        corr = pivot.corr()


        fig = px.imshow(
            corr,
            text_auto=".2f",
            template="plotly_dark",
            title="Sector Allocation Correlation"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


    # --------------------------------------------------
    # Polynomial Projection
    # --------------------------------------------------

    if not df_macro.empty:

        st.subheader(
            "Budget Projection"
        )


        degree = st.selectbox(
            "Polynomial Degree",
            [1, 2, 3],
            index=1
        )


        min_future_year = int(
            df_macro["year"].max() + 1
        )


        future = st.slider(
            "Forecast Year",
            min_future_year,
            2050,
            min(
                2035,
                2050
            )
        )


        x = df_macro["year"].values

        y = df_macro[
            "Total_Budget_Billions_USD"
        ].values


        if len(x) > degree:

            poly = np.poly1d(
                np.polyfit(
                    x,
                    y,
                    degree
                )
            )


            years = np.arange(
                x.max() + 1,
                future + 1
            )


            pred = poly(years)


            fig = go.Figure()


            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    mode="lines+markers",
                    name="Historical"
                )
            )


            if len(years) > 0:

                fig.add_trace(
                    go.Scatter(
                        x=years,
                        y=pred,
                        mode="lines",
                        line=dict(
                            dash="dash"
                        ),
                        name="Projection"
                    )
                )


            fig.update_layout(
                template="plotly_dark",
                title=f"{selected_country} Budget Projection",
                xaxis_title="Year",
                yaxis_title="Budget (Billion USD)"
            )


            st.plotly_chart(
                fig,
                width="stretch"
            )

        else:

            st.warning(
                "Not enough data points for this polynomial degree."
            )

