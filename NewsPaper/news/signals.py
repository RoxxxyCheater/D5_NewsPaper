from django.db.models.signals import post_save # сигнал после сохранения
from django.dispatch import receiver #функция получатель(декоратор)
from django.core.mail import mail_managers
# from django.core.signals import request_finished # сигнал окончания запроса к серверу
from .models import SubscribersMail
from django.template.loader import render_to_string # импортируем функцию, которая срендерит наш html в текст
from django.core.mail import EmailMultiAlternatives # импортируем класс для создание объекта письма с html 
from django.shortcuts import redirect

@receiver(post_save, sender=SubscribersMail) #sender - модель поста, instance - сущность поста который создаётся или сохраняется, created - есть ли такая сущность в бае данных(создаётся или отправляется)
def notifty_news_publicated(sender, instance, created, **kwargs):   #Функция коллбек - обработчик сигнала!
    if created:
        subject=f'{instance.subscriber}. Новая статья{instance.category} - {instance.client_title}!',
    else:
        subject=f'{instance.subscriber}. Статья изменена {instance.category} - {instance.client_title}!',

    # получем наш html
    html_content = render_to_string( 
        'subs_mail_created.html',
        {
            'newMailSub': instance,
        }
    )

    # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
    msg = EmailMultiAlternatives(
        subject=subject,
        body = instance.message, #  это то же, что и message
        from_email='lexinet3g@gmail.com',
        to=[instance.subscriber_email], # это то же, что и recipients_list
        #fail_silently=False нуен что бы всё не полетело в тартарары если что-то пошло не так - обязательно в продакшене
    )
    msg.attach_alternative(html_content, "text/html") # добавляем html
    #msg.send() # отсылаем

    # return redirect('/news')
  
  
  
    # коннектим наш сигнал к функции обработчику и указываем, к какой именно модели после сохранения привязать функцию
    #post_save.connect(notifty_news_publicated, sender=Post)
