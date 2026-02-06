def detect_bottlenecks(df):

    stage = df.groupby("stage_name")["approval_wait_hours"].mean()
    approver = df.groupby("approver_id")["approval_wait_hours"].mean()

    return stage.sort_values(ascending=False), approver.sort_values(ascending=False)
