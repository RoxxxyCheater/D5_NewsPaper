from hashlib import new
from apscheduler.schedulers.background import BackgroundScheduler

news_scheduler = BackgroundScheduler()
# news_scheduler.add_job( #Запускается(перенорсим в apps.py метод ready)
#     id = 'send_mail',#id func из tasks.py
#     func = lambda:print('123'), #что передать
#     trigger = 'interval', # определённый промежуток времени
#     seconds=5,
# )