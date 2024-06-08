from itertools import product

SIZES = [3, 5, 10, 15, 25]

def calculate_recall(predictions, labels):
    correct_predictions = sum(1 for label in labels if label in predictions)
    if labels:
        return correct_predictions / len(labels)
    return 0


def calculate_reciprocal_rank(predictions, labels):
    for index, prediction in enumerate(predictions):
        if prediction in labels:
            return 1 / (index + 1)
    return 0


metrics = {"mrr": calculate_reciprocal_rank, "recall": calculate_recall}


def score(preds, label):
    return {
        f"{fn_name}@{size}": round(metrics[fn_name](preds[:size], [label]), 3)
        for fn_name, size in product(metrics.keys(), SIZES)
    }