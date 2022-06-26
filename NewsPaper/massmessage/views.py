from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives # импортируем класс для создание объекта письма с html
from datetime import datetime
 
 
from django.template.loader import render_to_string # импортируем функцию, которая срендерит наш html в текст
from .models import Appointment
 
 
class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news.html', {})
 
    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_title=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()
 
        # получем наш html
        html_content = render_to_string( 
            'add_news.html',
            {
                'appointment': appointment,
            }
        )
 
        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_title} {appointment.date.strftime("%Y-%M-%d")}',
            body=appointment.message, #  это то же, что и message
            from_email='lexinet3g@gamil.com',
            to=['sayt@3g.ua'], # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html") # добавляем html

        msg.send() # отсылаем
 
        return redirect('appointments:make_appointment')