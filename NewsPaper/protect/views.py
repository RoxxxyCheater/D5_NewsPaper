from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView): # generic-представление для отображения шаблона унаследовав от LoginRequiredMixin
    template_name = '../templates/news.html'