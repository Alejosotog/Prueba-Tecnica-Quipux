from database.connection import hourly_reports_collection


def save_report(report):
    result = hourly_reports_collection.insert_one(report)
    return result


def get_reports():
    return list(
        hourly_reports_collection
        .find({})
        .sort("generated_at", -1)
    )