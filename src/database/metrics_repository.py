from database.connection import metrics_collection


def save_metrics(metrics):
    result = metrics_collection.insert_one(metrics)

    return result