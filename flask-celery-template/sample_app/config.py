class Config:
    SESSION_TYPE = "memcache"
    SECRET_KEY = "MY_SECRET_KEY"
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'