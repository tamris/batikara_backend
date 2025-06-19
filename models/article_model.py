from datetime import datetime
from bson import ObjectId
from zoneinfo import ZoneInfo

def article_serializer(article) -> dict:
    created_at = article.get("created_at")
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=ZoneInfo("UTC"))
    jakarta_time = created_at.astimezone(ZoneInfo("Asia/Jakarta"))

    return {
        "id": str(article["_id"]),
        "title": article["title"],
        "description": article["description"],
        "image_url": article["image_url"],
        "created_at": jakarta_time.strftime('%Y-%m-%d %H:%M:%S')
    }

def create_article_data(title, description, image_url):
    return {
        "title": title,
        "description": description,
        "image_url": image_url,
        "created_at": datetime.utcnow()
    }
