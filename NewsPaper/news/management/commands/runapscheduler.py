# runapscheduler.py
import logging
from multiprocessing.dummy import active_children
from re import sub
from unicodedata import category

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.template.loader import render_to_string # импортируем функцию, которая срендерит наш html в текст
from django.core.mail import EmailMultiAlternatives # импортируем класс для создание объекта письма с html 
from requests import request
from news.models import SubscribersMail
from news.models import Post,Author,Category, PostCategory, SubsCategory, User
from datetime import date, datetime,timedelta



logger = logging.getLogger(__name__) # Функция логгер дл того что бы выводилось сообщение мол,сервак запущен,все работает и т.д.


def my_job(): # Здесь код для выполнения поставленной задачи
  subscribers = SubsCategory.objects.all()
  users_active = []
  mydate = date.today()-timedelta(days=7)
  for sub_user in subscribers:
    if sub_user.subscribers_id not in users_active:
      recipient = User.objects.get(id = sub_user.subscribers_id)
      categorysId = SubsCategory.objects.filter(subscribers = sub_user.subscribers_id).values_list('category', flat=True) #.filter(created_at__gt = mydate)
      users_active.append(sub_user.subscribers_id)
      last_week = Post.objects.filter(created_at__gt = mydate, postCategory__in = categorysId)

      html_content = render_to_string( 
        'subs_mail_created.html',
        {
            'newMailSub': last_week,
        }
    )

      # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
      msg = EmailMultiAlternatives(
          subject= f'Dear subscriber - news from last week',
          body = last_week, #  это то же, что и message
          from_email='lexinet3g@gmail.com',
          to=[recipient.email], # это то же, что и recipients_list
          #fail_silently=False нуен что бы всё не полетело в тартарары если что-то пошло не так - обязательно в продакшене
      )
      msg.attach_alternative(html_content, "text/html") # добавляем html
      msg.send() # отсылаем












    
    # post_category = list(PostCategory.objects.filter(post = post).values().values('category_id').last().values())[0]
    # subscribe_category = Category.objects.get(id = post_category)
    # subscribersId = SubsCategory.objects.filter(category = post_category).values('subscribers')
    # sub_list.append(subscribersId)
    # if subscribersId not in sub_list:
    # user = 
    # Пользователи из моста
    # Итеруешь пользователей



# Я АЛЕКСЕЙ, А ТЫ НЕТ!

# Ка Бы небыло зимы в городах и сёлах
# никогда б не знали мы этих дней веселых
# Не возилась б детвора возле снежной бабы
# Не петляла бы лыжня кабы кабы кабы


# ты шо бля делаешь в моей голове?????







    #active_user = User.objects.filter(id= subscribersId).values()
    #SubsUser = User.objects.get(id = userID['subscribers'])
    #print(post_category, subscribe_category, subscribersId, )
  #print('quize')
    # if active_user not in (subscribe_category.catS_subscribers.all()):
    #     subscribe_category.catS_subscribers.add(active_user) #добавляем юзера
    # elif active_user in (subscribe_category.catS_subscribers.all()):
    #     subscribe_category.catS_subscribers.remove(active_user)

  
  # print(user_posts)
  # pass


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way. 
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
  """
  This job deletes APScheduler job execution entries older than `max_age` from the database.
  It helps to prevent the database from filling up with old historical records that are no
  longer useful.
  
  :param max_age: The maximum length of time to retain historical job execution records.
                  Defaults to 7 days.
  """
  DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
  help = "Runs APScheduler."

  def handle(self, *args, **options):
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE) # BlockingScheduler потому что он работает в отдельном потоке/
    #Scheduler только один и не имеет конкуренции и запускается отдельно от сервера
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
      my_job, # Вызов функции myjob()
      trigger=CronTrigger(second="*/1"),  # Every 10 seconds/почти тоже самое что интервал
      id="my_job",  # The `id` assigned to each job MUST be unique
      max_instances=1,
      replace_existing=True, # если такой таск есть,то он будет заменятся на новый
    )
    logger.info("Added job 'my_job'.")

    scheduler.add_job(
      delete_old_job_executions,
      trigger=CronTrigger(
        day_of_week="mon", hour="00", minute="00"
      ),  # Midnight on Monday, before start of the next work week.
      id="delete_old_job_executions",
      max_instances=1,
      replace_existing=True,
    )
    logger.info(
      "Added weekly job: 'delete_old_job_executions'."
    )

    try:
      logger.info("Starting scheduler...")
      scheduler.start()
    except KeyboardInterrupt:
      logger.info("Stopping scheduler...")
      scheduler.shutdown()
      logger.info("Scheduler shut down successfully!")


# import logging
 
# from django.conf import settings
 
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# from django.core.management.base import BaseCommand
# from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution
 
 
# logger = logging.getLogger(__name__)
 
 
# # наша задача по выводу текста на экран
# def my_job():
#     #  Your job processing logic here... 
#     print('hello from job')
 
 
# # функция которая будет удалять неактуальные задачи
# def delete_old_job_executions(max_age=604_800):
#     """This job deletes all apscheduler job executions older than `max_age` from the database."""
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
# class Command(BaseCommand):
#     help = "Runs apscheduler."
 
#     def handle(self, *args, **options):
#         scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")
        
#         # добавляем работу нашему задачнику
#         scheduler.add_job(
#             my_job,
#             trigger=CronTrigger(second="*/10"),  # Тоже самое что и интервал, но задача тригера таким образом более понятна django
#             id="my_job",  # уникальный айди
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added job 'my_job'.")
 
#         scheduler.add_job(
#             delete_old_job_executions,
#             trigger=CronTrigger(
#                 day_of_week="mon", hour="00", minute="00"
#             ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
#             id="delete_old_job_executions",
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info(
#             "Added weekly job: 'delete_old_job_executions'."
#         )
 
#         try:
#             logger.info("Starting scheduler...")
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("Stopping scheduler...")
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")