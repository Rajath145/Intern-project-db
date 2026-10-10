import sqlite3
import pandas as pd

def store_and_join_datasets(df_trades: pd.DataFrame, df_macro: pd.DataFrame, db_path="trading_pipeline.db"):
    conn = sqlite3.connect(db_path)
    df_trades.to_sql("historical_trades", conn, if_exists="replace", index=False)
    df_macro.to_sql("macro_events", conn, if_exists="replace", index=False)
    join_query = """
    SELECT 
        t.trade_id,
        t.timestamp,
        t.strategy_id,
        t.parameter_permutation,
        t.trade_pnl,
        m.event_name,
        m.actual,
        m.forecast
    FROM historical_trades t
    LEFT JOIN macro_events m 
        ON DATE(t.timestamp) = DATE(m.timestamp)
    """
    df_merged = pd.read_sql(join_query, conn)
    conn.close()
    
    return df_merged