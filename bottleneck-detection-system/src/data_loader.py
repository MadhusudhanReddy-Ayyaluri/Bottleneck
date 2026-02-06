import pandas as pd

def load_data(file):

    df = pd.read_csv(file)

    time_cols = [
        "start_time",
        "approval_request_time",
        "approval_granted_time",
        "end_time",
        "deadline"
    ]

    for col in time_cols:
        df[col] = pd.to_datetime(df[col])

    # approval wait
    df["approval_wait_hours"] = (
        df["approval_granted_time"] - df["approval_request_time"]
    ).dt.total_seconds() / 3600

    # total duration
    df["total_duration_hours"] = (
        df["end_time"] - df["start_time"]
    ).dt.total_seconds() / 3600

    # delay label
    df["delayed"] = (df["end_time"] > df["deadline"]).astype(int)

    return df
