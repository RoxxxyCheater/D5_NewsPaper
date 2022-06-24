from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import send_mail
from datetime import datetime
 
from .models import Appointment
 
 
class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})
 
    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),  #дата записи.
            client_name=request.POST['client_name'], #Имя клиента тема сообщения
            message=request.POST['message'], #сообщение передаёт краткую суть проблемы
        )
        appointment.save()
 
        # отправляем письмо
        send_mail( 
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',  # имя клиента и дата записи будут в теме для удобства
            message=appointment.message, # сообщение с кратким описанием проблемы
            from_email='peterbadson@yandex.ru', # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=[] # здесь список получателей. Например, секретарь, сам врач и так далее
        )
 
        return redirect('appointments:make_appointment')