from django.shortcuts import render

from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm

from django.shortcuts import redirect
from django.contrib.auth.models import Group #импортировать модель групп
from django.contrib.auth.decorators import login_required #декоратор проверки аутентификации


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news/'

@login_required
def upgrade_me(request):
    user = request.user # получили объект текущего пользователя из переменной запроса
    premium_group = Group.objects.get(name='authors') #Вытащили premium-группу из модели Group
    if not request.user.groups.filter(name='authors').exists(): #проверяем, находится ли пользователь в этой группе (вдруг кто-то решил перейти по этому URL, уже имея Premium)
        premium_group.user_set.add(user) #Если ещё не в ней — добавляем.
    return redirect('/') # перенаправляем пользователя на корневую страницу, используя метод redirect