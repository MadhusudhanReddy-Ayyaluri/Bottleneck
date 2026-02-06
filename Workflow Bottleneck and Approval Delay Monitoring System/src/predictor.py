from sklearn.ensemble import RandomForestClassifier

def train_model(df):

    features = [
        "approval_wait_hours",
        "workload_level",
        "total_duration_hours"
    ]

    X = df[features]
    y = df["delayed"]

    model = RandomForestClassifier(n_estimators=100)

    model.fit(X, y)

    return model
