import sqlalchemy
from sqlalchemy.orm import sessionmaker
from elasticsearch import Elasticsearch, helpers
from datetime import datetime
import logging

from doraSpider.models import Base, Post

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MySQL connection settings
MYSQL_URL = "mysql+pymysql://root:admin123@localhost:3306/dora?charset=utf8mb4"
ES_URL = "http://localhost:9200"
INDEX_NAME = "posts"


def create_es_index(es_client):
    """Create Elasticsearch index with IK analyzer if it doesn't exist"""
    index_settings = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "ik_max_word": {
                        "type": "ik_max_word"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "id": {"type": "long"},
                "content": {
                    "type": "text",
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_max_word"
                },
                "uid": {"type": "long"},
                "is_anonymous": {"type": "boolean"},
                "is_distinguished": {"type": "boolean"},
                "risky": {"type": "boolean"},
                "topic_id": {"type": "long"},
                "comment_sum": {"type": "integer"},
                "like_sum": {"type": "integer"},
                "hot": {"type": "integer"},
                "tip_sum": {"type": "integer"},
                "forward_sum": {"type": "integer"},
                "dun_num": {"type": "integer"},
                "school_id": {"type": "long"},
                "published_at": {"type": "date"},
                "is_ever_top": {"type": "boolean"},
                "ever_top_end_time": {"type": "date"},
                "sentiment_label": {"type": "integer"},
                "sentiment_confidence": {"type": "float"}
            }
        }
    }

    if not es_client.indices.exists(index=INDEX_NAME):
        es_client.indices.create(index=INDEX_NAME, body=index_settings)
        logger.info(f"Created Elasticsearch index: {INDEX_NAME}")
    else:
        logger.info(f"Index {INDEX_NAME} already exists")


def get_mysql_session():
    """Create MySQL session"""
    engine = sqlalchemy.create_engine(MYSQL_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def post_to_es_doc(post):
    """Convert Post object to Elasticsearch document"""
    print(post.sentiment_label)
    return {
        "_index": INDEX_NAME,
        "_id": str(post.id),
        "_source": {
            "id": post.id,
            "content": post.content,
            "uid": post.uid,
            "is_anonymous": post.is_anonymous,
            "is_distinguished": post.is_distinguished,
            "risky": post.risky,
            "topic_id": post.topic_id,
            "comment_sum": post.comment_sum,
            "like_sum": post.like_sum,
            "hot": post.hot,
            "tip_sum": post.tip_sum,
            "forward_sum": post.forward_sum,
            "dun_num": post.dun_num,
            "school_id": post.school_id,
            "settled": post.settled,
            "published_at": post.published_at.isoformat() if post.published_at else None,
            "is_ever_top": post.is_ever_top,
            "ever_top_end_time": post.ever_top_end_time.isoformat() if post.ever_top_end_time else None,
            "sentiment_label": post.sentiment_label,
            "sentiment_confidence": post.sentiment_confidence
        }
    }


def sync_to_es():
    """Sync MySQL posts to Elasticsearch"""
    try:
        # Initialize clients
        es_client = Elasticsearch([ES_URL])
        session = get_mysql_session()

        # Create index if it doesn't exist
        create_es_index(es_client)

        # Query all posts
        posts = session.query(Post).all()
        logger.info(f"Found {len(posts)} posts to sync")

        # Prepare bulk actions
        actions = [post_to_es_doc(post) for post in posts]

        # Perform bulk indexing
        if actions:
            success, failed = helpers.bulk(es_client, actions)
            logger.info(f"Successfully indexed {success} documents")
            if failed:
                logger.error(f"Failed to index {len(failed)} documents")
        else:
            logger.info("No posts to sync")

    except Exception as e:
        logger.error(f"Error during sync: {str(e)}")
    finally:
        session.close()


if __name__ == "__main__":
    sync_to_es()