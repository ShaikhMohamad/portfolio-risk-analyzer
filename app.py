import streamlit as st
import pandas as pd

from var_calculation import calculate_portfolio_var


# ============================================================
# 1. PAGE TITLE
# ============================================================

st.title("Portfolio Risk Analyzer")
st.subheader("Historical Value at Risk Analysis")


# ============================================================
# 2. LOAD DATA
# ============================================================

FILE_PATH = "data/portfolio_data.xlsx"

df = pd.read_excel(FILE_PATH)


# ============================================================
# 3. PORTFOLIO INVESTMENT
# ============================================================

st.subheader("Portfolio Investment")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    invest_TCS = st.number_input(
        "TCS",
        min_value=0.0,
        value=0.0
    )

with col2:
    invest_INFY = st.number_input(
        "INFY",
        min_value=0.0,
        value=0.0
    )

with col3:
    invest_HCL = st.number_input(
        "HCLTECH",
        min_value=0.0,
        value=0.0
    )

with col4:
    invest_TECHM = st.number_input(
        "TECHM",
        min_value=0.0,
        value=0.0
    )

with col5:
    invest_WIPRO = st.number_input(
        "WIPRO",
        min_value=0.0,
        value=0.0
    )


# ============================================================
# 4. CONFIDENCE LEVEL
# ============================================================

confidence = st.radio(
    "Select Confidence Level",
    [95, 99],
    horizontal=True
)


# ============================================================
# 5. INVESTMENT DICTIONARY
# ============================================================

investments = {
    "TCS": invest_TCS,
    "INFY": invest_INFY,
    "HCLTECH": invest_HCL,
    "TECHM": invest_TECHM,
    "WIPRO": invest_WIPRO
}


# ============================================================
# 6. TOTAL INVESTMENT
# ============================================================

total_investment = sum(investments.values())


# ============================================================
# 7. PORTFOLIO CALCULATION
# ============================================================

if total_investment > 0:

    results = calculate_portfolio_var(
        df,
        investments,
        confidence
    )

    weights = results["weights"]

    var_1d = results["var_1d"]
    var_5d = results["var_5d"]
    var_20d = results["var_20d"]


    # ========================================================
    # 8. PORTFOLIO SUMMARY
    # ========================================================

    st.subheader("Portfolio Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Investment",
            f"₹{total_investment:,.2f}"
        )

    with col2:
        st.metric(
            "Number of Stocks",
            "5"
        )

    with col3:
        st.metric(
            "Confidence Level",
            f"{confidence}%"
        )


    # ========================================================
    # 9. PORTFOLIO WEIGHTS
    # ========================================================

    st.write("### Portfolio Weights")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "TCS",
            f"{weights['TCS']:.2%}"
        )

    with col2:
        st.metric(
            "INFY",
            f"{weights['INFY']:.2%}"
        )

    with col3:
        st.metric(
            "HCLTECH",
            f"{weights['HCLTECH']:.2%}"
        )

    with col4:
        st.metric(
            "TECHM",
            f"{weights['TECHM']:.2%}"
        )

    with col5:
        st.metric(
            "WIPRO",
            f"{weights['WIPRO']:.2%}"
        )


    # ========================================================
    # 10. HISTORICAL VaR RESULTS
    # ========================================================

    st.subheader("Historical VaR Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "1-Day VaR",
            f"₹{var_1d:,.2f}"
        )

    with col2:
        st.metric(
            "5-Day VaR",
            f"₹{var_5d:,.2f}"
        )

    with col3:
        st.metric(
            "20-Day VaR",
            f"₹{var_20d:,.2f}"
        )


    st.write(
        f"Historical VaR calculated at "
        f"{confidence}% confidence level."
    )


else:

    st.info(
        "Enter investment amounts above to calculate portfolio VaR."
    )


# ============================================================
# 11. DATA INFORMATION
# ============================================================

with st.expander("View Historical Data"):

    st.write(
        f"Dataset contains {len(df):,} rows "
        f"and {len(df.columns)} columns."
    )

    st.dataframe(df)