from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView): # generic-представление для отображения шаблона унаследовав от LoginRequiredMixin
    template_name = '../templates/news.html'

    def get_context_data(self, **kwargs): #переопределяем метод получения контекста
        context = super().get_context_data(**kwargs) #получили весь контекст из класса-родителя
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        #добавили новую контекстную переменную is_no t_premium
        #есть ли пользователь в группе - заходим в переменную запроса self.request/
        #Из этой переменной мы можем вытащить текущего пользователя
        #В поле groups хранятся все группы, в которых он состоит
        #применяем фильтр к этим группам и ищем ту самую, имя которой premium.
        #проверяем, есть ли какие-то значения в отфильтрованном списке.
        #Mетод exists() вернёт True, если группа premium в списке групп пользователя найдена
        #нам нужно получить наоборот — True, если пользователь не находится в этой группе, поэтому добавляем отрицание not
        return context #возвращаем контекст обратно