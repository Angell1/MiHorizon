from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('proj',
            broker = 'amqp://ling:123456@123.207.251.121:5672',
            backend = 'rpc://amqp://ling:123456@123.207.251.121:5672',
            include = ['celery_task.tasks'])

app.conf.update(
    result_expires = 3600
)

if __name__ == '__main__':
    app.start()