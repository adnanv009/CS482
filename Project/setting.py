# Django-Q Configuration
Q_CLUSTER = {
    'name': 'project_',  # Adjust as necessary
    'workers': 4,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'cpu_affinity': 1,
    'save_limit': 250,
    'orm': 'default',
}

# Celery Configuration
CELERY_BROKER_URL = 'amqp://localhost'  # Use RabbitMQ or Redis URL here
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
