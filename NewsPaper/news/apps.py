from sched import scheduler
from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self): #Подходит для тасков из Вьюх!
        import news.signals 
        ##############################
        #scheduler tasks
        # from .tasks import send_mail #импортируем функицю отправить мэйл из таскс
        # from .scheduler import news_scheduler 
        # print('!!!started tasks')
        
        # news_scheduler.add_job(
        #     id = 'send_mail',#id func из tasks.py
        #     func = send_mail, #lambda:print('123'), #что передать
        #     trigger = 'interval', # определённый промежуток времени
        #     seconds=5,
        # )
        # news_scheduler.start() #Что бы не дублировалось py NewsPaper/manage.py runserver  --noreload



    