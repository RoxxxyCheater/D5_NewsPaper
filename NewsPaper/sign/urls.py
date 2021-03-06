from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView
from .views import upgrade_me

urlpatterns = [
     path('login/', 
         LoginView.as_view(template_name = '../templates/sign/login.html'), #фреймворк предоставляет готовое представление на основе классов LoginView
         name='login'),
     path('logout/', 
         LogoutView.as_view(template_name = '../templates/sign/login.html'), #При выходе с сайта (кнопка в шаблоне index.html) Django перенаправит пользователя на страницу, указанную в параметре template_name класса LogoutView.
         name='logout'),
     path('signup/', 
         BaseRegisterView.as_view(template_name = 'sign/signup.html'), 
         name='signup'),
     path('upgrade/', upgrade_me, name = 'upgrade'),
     path('accounts/', include('allauth.urls')),
]