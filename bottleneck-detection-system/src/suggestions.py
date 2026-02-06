def generate_suggestions(stage, approver):

    suggestions = []

    if len(stage) > 0 and stage.iloc[0] > 2:
        suggestions.append("High delay stage → add extra reviewers")

    if len(approver) > 0 and approver.iloc[0] > 2:
        suggestions.append("Approver overloaded → assign backup approver")

    suggestions.append("Prioritize urgent approvals automatically")

    return suggestions
