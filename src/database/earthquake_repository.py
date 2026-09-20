from database.connection import earthquakes_collection


def save_earthquake(earthquake):
    document = earthquake.model_dump()

    result = earthquakes_collection.update_one(
        {"event_id": earthquake.event_id},
        {"$set": document},
        upsert=True
    )

    return result.upserted_id is not None