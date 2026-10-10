import numpy as np
import pandas as pd
import xgboost as xgb
def walk_forward_validation(df, train_window=1000, test_window=200):
    results = []

    for i in range(train_window, len(df) - test_window, test_window):
        train, test = df.iloc[i-train_window:i], df.iloc[i:i+test_window]

        model = xgb.XGBClassifier(n_estimators=100, learning_rate=0.05, max_depth=4)
        model.fit(train[["surprise_metric", "hour", "day_of_week"]], train["is_win"])

        results.append({
            "fold_start": test.index[0],
            "accuracy": accuracy_sc(
                test["is_win"],
                model.predict(test[["surprise_metric", "hour", "day_of_week"]])
            )
        })

    return pd.DataFrame(results)