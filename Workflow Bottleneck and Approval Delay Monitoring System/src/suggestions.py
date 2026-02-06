def generate_suggestions(pending_count):
    suggestions = []

    if pending_count > 0:
        suggestions.append("There are pending approvals blocking employees.")

    if pending_count > 3:
        suggestions.append("Consider assigning backup approvers.")

    suggestions.append("Review approvals daily to avoid delays.")

    return suggestions
