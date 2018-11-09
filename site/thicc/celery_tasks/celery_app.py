from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thicc.settings')


#if os.getenv('IS_DEVELOPMENT', False) or settings.DEBUG:
BROKER_URL = [
    # 'redis://%s:6379/0' % url
    #'amqp://guest@localhost//' # for non dockerized rabbitmq
    'amqp://{}:{}@rabbitmq//'.format(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD) # for dockerized rabbitmq
]
#else:
#    BROKER_URL = [
#        'amqp://%s:%s@rmq-0.rmq.default.svc.cluster.local:5672/%s' % (settings.RABBIT_USER, settings.RABBIT_PASSWORD, settings.RABBIT_VHOST) ,
#        'amqp://%s:%s@rmq-1.rmq.default.svc.cluster.local:5672/%s' % (settings.RABBIT_USER, settings.RABBIT_PASSWORD, settings.RABBIT_VHOST) ,
#        'amqp://%s:%s@rmq-2.rmq.default.svc.cluster.local:5672/%s' % (settings.RABBIT_USER, settings.RABBIT_PASSWORD, settings.RABBIT_VHOST) ,
#    ]

app = Celery('thicc', broker=BROKER_URL)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# if settings.IS_PROD:
#     url = os.getenv('PROD_REDIS_MASTER_SERVICE_HOST', 'localhost')
# else:
#     url = os.getenv('DEV_REDIS_MASTER_SERVICE_HOST', 'localhost')
# app.conf.broker_url = 'redis://%s:6379/0' % url




# # Load task modules from all registered Django app configs.
app.autodiscover_tasks()
#
#
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
