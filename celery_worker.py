from celery import Celery

celery_app = Celery(
    "blood_test_analyser",
    broker="redis://:PQOF9aW386wTkiZHM1JnJAfA4QVqUMDK@redis-10036.c267.us-east-1-4.ec2.redns.redis-cloud.com:10036/0",
    backend="redis://:PQOF9aW386wTkiZHM1JnJAfA4QVqUMDK@redis-10036.c267.us-east-1-4.ec2.redns.redis-cloud.com:10036/0"
)