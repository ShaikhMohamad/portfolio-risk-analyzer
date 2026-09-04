import pandas as pd


# ============================================================
# RETURN COLUMNS
# ============================================================

daily_cols = [
    "TCS_Return",
    "INFY_Return",
    "HCLTECH_Return",
    "TECHM_Return",
    "WIPRO_Return"
]

cols_5d = [
    "TCS_5D_Return",
    "INFY_5D_Return",
    "HCLTECH_5D_Return",
    "TECHM_5D_Return",
    "WIPRO_5D_Return"
]

cols_20d = [
    "TCS_20D_Return",
    "INFY_20D_Return",
    "HCLTECH_20D_Return",
    "TECHM_20D_Return",
    "WIPRO_20D_Return"
]


# ============================================================
# HISTORICAL VaR CALCULATION
# ============================================================

def calculate_var(pnl_series, confidence):

    confidence_decimal = confidence / 100

    return abs(
        pnl_series.quantile(
            1 - confidence_decimal
        )
    )


# ============================================================
# PORTFOLIO VaR
# ============================================================

def calculate_portfolio_var(
    df,
    investments,
    confidence
):

    # --------------------------------------------------------
    # Total Investment
    # --------------------------------------------------------

    total_investment = sum(investments.values())

    if total_investment <= 0:
        return None


    # --------------------------------------------------------
    # Portfolio Weights
    # --------------------------------------------------------

    weights = {
        stock: investment / total_investment
        for stock, investment in investments.items()
    }


    # --------------------------------------------------------
    # Prepare Data
    # --------------------------------------------------------

    df_1d = df.dropna(
        subset=daily_cols
    ).copy()

    df_5d = df.dropna(
        subset=cols_5d
    ).copy()

    df_20d = df.dropna(
        subset=cols_20d
    ).copy()


    # ========================================================
    # Portfolio Returns
    # ========================================================

    df_1d["Portfolio_Return"] = (
        df_1d["TCS_Return"] * weights["TCS"]
        + df_1d["INFY_Return"] * weights["INFY"]
        + df_1d["HCLTECH_Return"] * weights["HCLTECH"]
        + df_1d["TECHM_Return"] * weights["TECHM"]
        + df_1d["WIPRO_Return"] * weights["WIPRO"]
    )

    df_5d["Portfolio_5D_Return"] = (
        df_5d["TCS_5D_Return"] * weights["TCS"]
        + df_5d["INFY_5D_Return"] * weights["INFY"]
        + df_5d["HCLTECH_5D_Return"] * weights["HCLTECH"]
        + df_5d["TECHM_5D_Return"] * weights["TECHM"]
        + df_5d["WIPRO_5D_Return"] * weights["WIPRO"]
    )

    df_20d["Portfolio_20D_Return"] = (
        df_20d["TCS_20D_Return"] * weights["TCS"]
        + df_20d["INFY_20D_Return"] * weights["INFY"]
        + df_20d["HCLTECH_20D_Return"] * weights["HCLTECH"]
        + df_20d["TECHM_20D_Return"] * weights["TECHM"]
        + df_20d["WIPRO_20D_Return"] * weights["WIPRO"]
    )


    # ========================================================
    # Portfolio P&L
    # ========================================================

    df_1d["Portfolio_PnL"] = (
        df_1d["Portfolio_Return"]
        * total_investment
    )

    df_5d["Portfolio_PnL_5D"] = (
        df_5d["Portfolio_5D_Return"]
        * total_investment
    )

    df_20d["Portfolio_PnL_20D"] = (
        df_20d["Portfolio_20D_Return"]
        * total_investment
    )


    # ========================================================
    # VaR
    # ========================================================

    var_1d = calculate_var(
        df_1d["Portfolio_PnL"],
        confidence
    )

    var_5d = calculate_var(
        df_5d["Portfolio_PnL_5D"],
        confidence
    )

    var_20d = calculate_var(
        df_20d["Portfolio_PnL_20D"],
        confidence
    )


    # ========================================================
    # Return Results
    # ========================================================

    return {
        "total_investment": total_investment,
        "weights": weights,
        "var_1d": var_1d,
        "var_5d": var_5d,
        "var_20d": var_20d
    }