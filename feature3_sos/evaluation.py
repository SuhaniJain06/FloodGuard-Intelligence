def evaluate_prediction(predicted, actual):
    results = {}

    for field in actual:
        results[field] = predicted.get(field) == actual[field]

    return results