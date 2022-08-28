from email import message
from genericpath import exists
from hashlib import new
from unicodedata import category
from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView,CreateView,UpdateView, DeleteView # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.core.paginator import Paginator # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from requests import request #проверка используется для того, чтобы разрешить доступ к странице, которая доступна только для зарегистрированных пользователей.
from .models import Post,Author,Category, PostCategory, SubsCategory
from datetime import date , datetime
from django.views import View # импортируем простую вьюшку
from .filters import NewsFilter # импортируем фильтр
from .forms import PostForm # импортируем форму
from django.contrib.auth.mixins import PermissionRequiredMixin #Миксин Ограничение прав доступа
from django.views.generic.edit import CreateView
from django.core.cache import cache # импортируем наш кэш
from django.template.loader import render_to_string # импортируем функцию, которая срендерит наш html в текст
from .models import SubscribersMail
from .exception import *
import logging
logger = logging.getLogger(__name__)
class PostList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news_all.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news_all'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-id') # По такому запросу сформируется список объектов, которые будут выводиться в представлении/если не указывать по умолчанию сработает не .order_by('-id'), а .all()
    #ordering = ['-id'] #сортировка от нового к старому
    paginate_by = 10

    logger.debug('DEBUG level')
    logger.info('INFO level')
    logger.warning('WARNING level')
    logger.error('ERROR level')
    logger.critical('CRITICAL level')

    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        
        return context    
    
    def get_context_data(self, **kwargs): #переопределяем метод получения контекста
        context = super().get_context_data(**kwargs) #получили весь контекст из класса-родителя
        context['is_authors'] = self.request.user.groups.filter(name = 'authors').exists()
        context['user_info'] = self.request.user
        #добавили новую контекстную переменную is_authors
        #есть ли пользователь в группе - заходим в переменную запроса self.request/
        #Из этой переменной мы можем вытащить текущего пользователя
        #В поле groups хранятся все группы, в которых он состоит
        #применяем фильтр к этим группам и ищем ту самую, имя которой premium.
        #проверяем, есть ли какие-то значения в отфильтрованном списке.
        #Mетод exists() вернёт True, если группа premium в списке групп пользователя найдена
        #нам нужно получить наоборот — True, если пользователь не находится в этой группе, поэтому добавляем отрицание not
        return context #возвращаем контекст обратно


class PostDetail(DetailView): # адресс в котором будет лежать информация о конкретной новости
    model = Post
    template_name ='news.html'
    context_object_name = 'news'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs): # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'{self.kwargs["pk"]}', None) # кэш очень похож на словарь, и метод get действует также. Он забирает значение по ключу, если его нет, то забирает None.
 
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset) 
            cache.set(f'{self.kwargs["pk"]}', obj)
            
        return obj


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (полиморфизм)
        # context['time_now'] = datetime.utcnow() # добавим переменную текущей даты time_now
        top_rated = Author.objects.all().order_by('-rateAuthor').values('authors', 'rateAuthor')[0]
        context['value1'] = {(User.objects.get(id=list(top_rated.values())[0])).username}, {list(top_rated.values())[1]} # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        context['category'] = Post.category
        context['category_none'] = False
        context['category_subscribers_is']  = False
        if self.request.GET.get('postCategory') is not None:
            context['category_none']  = True
            context['postCategory'] = Category.objects.filter(id = self.request.GET['postCategory']).first
            if Category.objects.get(id = self.request.GET['postCategory']) is not None: #DoesNotExist
                context['category_subscribers_is']  = True
                context['subscribers'] = []
                context['subscribers_email'] = []
                list_subscribers = SubsCategory.objects.filter(category_id = self.request.GET['postCategory']).values()
                for user in list_subscribers.values():
                    context['subscribers'].append(((User.objects.filter(id=list(user.values())[2])).first()).username)
                    context['subscribers_email'].append(((User.objects.filter(id=list(user.values())[2])).first()).email)
                context['user_unsubscribed'] = False if self.request.user.username in context['subscribers'] else True
                context['subscribe_user_obj'] = (Category.objects.get(id = self.request.GET['postCategory'])).catS_subscribers.values()
                context['authors'] = Author.objects.all()
            
        return context





class Posts(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 50
    ordering = ['-postRate']
    form_class = PostForm
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (полиморфизм)
        context['time_now'] = datetime.utcnow() # добавим переменную текущей даты time_now
        top_rated = Author.objects.all().order_by('-rateAuthor').values('authors', 'rateAuthor')[0]
        context['value1'] = {(User.objects.get(id=list(top_rated.values())[0])).username}, {list(top_rated.values())[1]} # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        context['category'] = Post.category
        context['category_none'] = False
        context['category_subscribers_is']  = False
        if self.request.GET.get('postCategory') is not None:
            context['category_none']  = True
            context['postCategory'] = Category.objects.filter(id = self.request.GET['postCategory']).first
            if Category.objects.get(id = self.request.GET['postCategory']) is not None: #DoesNotExist
                context['category_subscribers_is']  = True
                context['subscribers'] = []
                context['subscribers_email'] = []
                list_subscribers = SubsCategory.objects.filter(category_id = self.request.GET['postCategory']).values()
                for user in list_subscribers.values():
                    context['subscribers'].append(((User.objects.filter(id=list(user.values())[2])).first()).username)
                    context['subscribers_email'].append(((User.objects.filter(id=list(user.values())[2])).first()).email)
                context['user_unsubscribed'] = False if self.request.user.username in context['subscribers'] else True
                context['subscribe_user_obj'] = (Category.objects.get(id = self.request.GET['postCategory'])).catS_subscribers.values()
                context['authors'] = Author.objects.all()
            
        return context
    
    def post(self, request, *args, **kwargs):
        # берём выбранную категорию из POST-запроса отправленного на сервер и активного пользователя и добавляем в поле Category.subscribe_category нового подписчика
        PostCategory = request.GET.get('postCategory')
        active_user = request.user #получаем юзера из реквеста
        subscribe_category = Category.objects.get(id = PostCategory) # получаем категорию
        try:
            if active_user not in (subscribe_category.catS_subscribers.all()):
                subscribe_category.catS_subscribers.add(active_user) #добавляем юзера
            elif active_user in (subscribe_category.catS_subscribers.all()):
                subscribe_category.catS_subscribers.remove(active_user)
            else:
                raise Exception.UserSubscribNotFound
        except Exception.UserSubscribNotFound:
            print('!!!!!!!!!!!!!!!!!!!!!!Ошибка запроса!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        subscribe_category.save()
        return redirect('/news/search')# отправляем пользователя обратно на GET-запрос.
    

class PostsView(View):

    def get(self, request):
        posts = Post.objects.order_by('-postRate')
        paginator = Paginator(posts, 3) # создаём объект класса пагинатор, передаём ему список наших товаров и их количество для одной страницы
        posts = paginator.get_page(request.GET.get('page', 1))  #берём номер страницы из get-запроса. Если ничего не передали, будем показывать первую страницу.
        
        # теперь вместо всех объектов в списке товаров хранится только нужная нам страница с товарами 
        data = {
            'posts': posts,
        }
        #return render(request, 'news/post_list.html', data)
        return render(request, 'search.html', data)
    

class PostAdd(PermissionRequiredMixin, CreateView):
    template_name = 'add_news.html'

    form_class = PostForm
    permission_required = 'news.add_news'
    raise_exception = True


    def has_permission(self):
        user_is_author = self.request.user.groups.filter(name = 'authors').exists()
        return user_is_author
    
    def author_add(self, request):
        if request.method == 'POST':
            new_author = Author(authors =User.objects.get(username=request.POST.get('username')))

        print(self,request )
        return new_author
        
    def post(self, request, *args, **kwargs): # сохраняем запрос
        #author_add()
        user_posts = Post.objects.filter(created_at__gte = date.today(), author = request.POST['author'])
        print('WWWWWWWWWWWWWWW - user_posts: ', len(user_posts),user_posts)
        if len(user_posts) > 3: #лимит в три новости в день на автора
            return redirect('/news/search')# отправляем пользователя обратно на GET-запрос.
        post_save_request = super().post(request, *args, **kwargs)
        postCats=request.POST['postCategory']
        subscribersId = SubsCategory.objects.filter(category = postCats).values('subscribers')
        mail_title = request.POST['title']
        mail_text = request.POST['content']
        link = post_save_request.url
        print(link, request.POST)
        category = Category.objects.filter(id = postCats).first()
        #Для лимита в три поста #
        
        #вытянуть все посты юзера
        #last_posts = list(user_posts)[:3].sort()
        #print('@@@@@!!!!!!!!!!!!last_posts: ',last_posts)
        #отсортировать по свежести
        #если есть новее суток
        #вернуть тру или фолс если меньше трёх ничего
        #else отменить сохранение
        #
        #

        for userID in subscribersId:
            SubsUser = User.objects.get(id = userID['subscribers'])
            print(SubsUser)
            newMailSub = SubscribersMail(
                client_title = mail_title,
                message= mail_text,
                category =  category,
                href = f'http://127.0.0.1:8000' + link,
                subscriber = SubsUser.username,
                subscriber_email = SubsUser.email
            )
            #print('@@@@',newMailSub, '@@@@', newMailSub.client_title, '@@@@', newMailSub.message, '@@@@', newMailSub.category, '@@@@', newMailSub.subscriber, '@@@@', newMailSub.subscriber_email)
            newMailSub.save()

            # # получем наш html
            # html_content = render_to_string( 
            #     'subs_mail_created.html',
            #     {
            #         'newMailSub': newMailSub,
            #     }
            # )
    
            # # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
            # msg = EmailMultiAlternatives(
            #     subject=f'Здравствуй, {newMailSub.subscriber}. Новая статья в твоём любимом разделе {newMailSub.category} - {newMailSub.client_title}!',
            #     body = newMailSub.message, #  это то же, что и message
            #     from_email='lexinet3g@gamil.com',
            #     to=[SubsUser.email], # это то же, что и recipients_list
            #     #fail_silently=False нуен что бы всё не полетело в тартарары если что-то пошло не так - обязательно в продакшене
            # )
            # msg.attach_alternative(html_content, "text/html") # добавляем html

            # msg.send() # отсылаем
    
        return post_save_request

# дженерик для редактирования объекта
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'post_update.html'
    form_class = PostForm
    model = Post
    permission_required = 'news.post_update'
    raise_exception = True

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
    
    def has_permission(self):
        has_perms = super().has_permission()
        self.object = self.get_object()
        user_is_author = self.request.user.groups.filter(name = 'authors').exists()
        return has_perms or user_is_author

 
 
# дженерик для удаления товара
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = 'news.post_delete'
    raise_exception = True

    def has_permission(self):
        has_perms = super().has_permission()
        self.object = self.get_object()
        user_is_author = self.request.user.groups.filter(name = 'authors').exists()
        return has_perms or user_is_author

 



 


