# В идеале, конечно, скрипты, относящиеся к формам, нужно хранить в отдельном файле forms.py, но для нас сейчас это не является принципиальным.

from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm #импортировали класс формы, который предоставляет allauth
from django.contrib.auth.models import Group # импортировали модель групп

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username", 
                  "first_name", 
                  "last_name", 
                  "email", 
                  "password1", 
                  "password2", )

class BasicSignupForm(SignupForm):#В кастом классе формы,(добавлять пользователя в группу) переопределяем только метод save(), который выполняется при успешном заполнении формы регистрации.

    def save(self, request):
        user = super(BasicSignupForm, self).save(request) #вызываем метод класса-родителя SignupForm, чтобы необходимые проверки и сохранение в модель User были выполнены.
        basic_group = Group.objects.get(name='users') # получаем объект модели группы basic
        basic_group.user_set.add(user) # через атрибут user_set, возвращающий список всех пользователей этой группы, мы добавляем нового пользователя в эту группу
        return user #Обязательным требованием метода save() является возвращение объекта модели User по итогу выполнения функции.