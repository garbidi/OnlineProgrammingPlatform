import random
from bson.objectid import ObjectId

def generate_task(template):
    variables = {}
    for i in range(1, 5):
        var_name = f"num{i}"
        if var_name in template["content"]:
            variables[var_name] = random.randint(10, 100)
    return template["content"].format(**variables)

def get_random_template(db, lesson_id, topic_id, page_type):
    template_cursor = db.templates.aggregate([
        {"$match": {
            "lesson_id": lesson_id,
            "topic_id": ObjectId(topic_id),
            "type": page_type
        }},
        {"$sample": {"size": 1}}
    ])
    try:
        return next(template_cursor)
    except StopIteration:
        return None
