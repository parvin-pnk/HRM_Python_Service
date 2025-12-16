def classify_complexity(estimated_effort: float):
    if estimated_effort < 2:
        return "Easy", max(1, min(3, round(estimated_effort * 1.5)))

    if estimated_effort < 6:
        return "Medium", max(4, min(7, round(estimated_effort * 1.2)))

    return "Hard", max(8, min(10, round(estimated_effort * 1.1)))
