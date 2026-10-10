import pandas as pd
def engineer_features(df):
    df["actual"] = pd.to_numeric(df["actual"], errors="coerce")
    df["forecast"] = pd.to_numeric(df["forecast"], errors="coerce")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df["surprise_metric"] = df["actual"] - df["forecast"]
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["is_win"] = (df["trade_pnl"] > 0).astype(int)

    return df.dropna(subset=["surprise_metric", "trade_pnl"])