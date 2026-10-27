"""
MongoDB client for ElectroStore
Handles chat logs and feedback storage
"""
import logging
from django.conf import settings

logger = logging.getLogger('chat')

_mongo_client = None
_mongo_db = None


def get_mongodb():
    """Get MongoDB database connection (lazy initialization)"""
    global _mongo_client, _mongo_db

    if not settings.MONGODB_URI:
        logger.warning("MONGODB_URI not configured - chat logs will not be persisted")
        return None

    if _mongo_db is not None:
        return _mongo_db

    try:
        from pymongo import MongoClient
        _mongo_client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000)
        _mongo_db = _mongo_client[settings.MONGODB_DB_NAME]
        # Verify connection
        _mongo_db.command('ping')
        logger.info("MongoDB connection established successfully")
        return _mongo_db
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
        _mongo_db = None
        return None


def save_chat_log(session_id, user_message, bot_response, feedback=None):
    """Save a chat interaction to MongoDB"""
    import datetime

    db = get_mongodb()
    if db is None:
        return None

    try:
        doc = {
            'session_id': session_id,
            'user_message': user_message,
            'bot_response': bot_response,
            'feedback': feedback,
            'timestamp': datetime.datetime.utcnow(),
        }
        result = db.chat_logs.insert_one(doc)
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Failed to save chat log: {e}")
        return None


def save_feedback(log_id, rating, comment=''):
    """Save user feedback for a chat interaction to MongoDB"""
    import datetime
    from bson import ObjectId

    db = get_mongodb()
    if db is None:
        return False

    try:
        db.chat_logs.update_one(
            {'_id': ObjectId(log_id)},
            {'$set': {
                'feedback': {'rating': rating, 'comment': comment},
                'feedback_at': datetime.datetime.utcnow()
            }}
        )
        return True
    except Exception as e:
        logger.error(f"Failed to save feedback: {e}")
        return False


def get_chat_history(session_id, limit=20):
    """Get chat history for a session from MongoDB"""
    db = get_mongodb()
    if db is None:
        return []

    try:
        logs = list(db.chat_logs.find(
            {'session_id': session_id},
            {'_id': 0, 'user_message': 1, 'bot_response': 1, 'timestamp': 1}
        ).sort('timestamp', -1).limit(limit))
        return logs
    except Exception as e:
        logger.error(f"Failed to get chat history: {e}")
        return []
