
pip install celery
#Конфигурация Django для соединения всех компонентов системы:
#В файле настроек Django (settings.py), добавьте следующие настройки для подключения Celery и Redis:
# Настройки Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# Настройки асинхронной рассылки уведомлений (Celery)
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULE = {
    'send_notifications': {
        'task': 'news_portal.tasks.send_notifications',
        'schedule': crontab(day_of_week='monday', hour=8),
    },
}
# Настройки Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
#Реализация рассылки уведомлений подписчикам после создания новости:
#Создайте файл tasks.py внутри приложения news_portal и определите в нем функцию send_notifications, которая будет отвечать за рассылку уведомлений подписчикам. Например:
from celery import shared_task
@shared_task
def send_notifications():
    # Получить список всех подписчиков
    subscribers = Subscriber.objects.all()
    for subscriber in subscribers:
        # Отправить уведомление подписчику
        send_notification(subscriber.email, 'Новостной портал', 'У вас новая новость!')
#Реализация еженедельной рассылки с последними новостями:
#Аналогично предыдущему шагу, создайте функцию send_weekly_newsletter в файле tasks.py, которая будет отправлять еженедельную рассылку с последними новостями. Например:
from celery import shared_task
from datetime import datetime, timedelta
@shared_task
def send_weekly_newsletter():
    # Получить последние новости за последнюю неделю
    last_week = datetime.now() - timedelta(days=7)
    latest_news = News.objects.filter(created_at__gte=last_week)
    # Отправить рассылку с новостями подписчикам
    for subscriber in Subscriber.objects.all():
        send_newsletter(subscriber.email, latest_news)
 #Запуск Celery:
#Запустите Celery для обработки задач в фоновом режиме. В командной строке, в корневой директории вашего проекта, выполните команду:
celery -A [имя_вашего_проекта] worker --loglevel=info
#Настройка периодической рассылки:
#Добавьте celery beat в вашу систему, чтобы запускать задачу регулярно. В командной строке, в корневой директории вашего проекта, выполните команду:
celery -A [имя_вашего_проекта] beat --loglevel=info
