def top_students(mongo_collection):
    """Return all students sorted by average score"""
    return list(mongo_collection.aggregate([
        {
            "$addFields": {
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]))
