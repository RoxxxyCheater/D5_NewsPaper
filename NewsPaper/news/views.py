from django.shortcuts import render
from django.views.generic import ListView, DetailView,CreateView,UpdateView, DeleteView # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.core.paginator import Paginator # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin #проверка используется для того, чтобы разрешить доступ к странице, которая доступна только для зарегистрированных пользователей.
from .models import Post,Author,Category, PostCategory, SubsCategory
from datetime import datetime
from django.views import View # импортируем простую вьюшку
from .filters import NewsFilter # импортируем фильтр
from .forms import PostForm # импортируем форму
from django.contrib.auth.mixins import PermissionRequiredMixin #Миксин Ограничение прав доступа
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
 
class PostList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news_all.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news_all'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-id') # По такому запросу сформируется список объектов, которые будут выводиться в представлении/если не указывать по умолчанию сработает не .order_by('-id'), а .all()
    #ordering = ['-id'] #сортировка от нового к старому
    paginate_by = 10
    
    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        return context    
    
    def get_context_data(self, **kwargs): #переопределяем метод получения контекста
        context = super().get_context_data(**kwargs) #получили весь контекст из класса-родителя
        context['is_authors'] = self.request.user.groups.filter(name = 'authors').exists()
        context['user_info'] = self.request.user
        #добавили новую контекстную переменную is_no t_premium
        #есть ли пользователь в группе - заходим в переменную запроса self.request/
        #Из этой переменной мы можем вытащить текущего пользователя
        #В поле groups хранятся все группы, в которых он состоит
        #применяем фильтр к этим группам и ищем ту самую, имя которой premium.
        #проверяем, есть ли какие-то значения в отфильтрованном списке.
        #Mетод exists() вернёт True, если группа premium в списке групп пользователя найдена
        #нам нужно получить наоборот — True, если пользователь не находится в этой группе, поэтому добавляем отрицание not
        return context #возвращаем контекст обратно


class PostDetail(DetailView): # адресс в котором будет лежать информация о конкретном товаре
    model = Post
    template_name ='news.html'
    context_object_name = 'news'


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
        context['value1'] = {User.objects.get(id=list(top_rated.values())[0])}, {list(top_rated.values())[1]} # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        context['category'] = Post.category
        context['category_none']  = False
        # if self.request.method is not None:
        #     context['category_none']  = True
        # context['postCategory'] = Category.objects.filter(id = self.request.GET['postCategory']).first #Post.postCategory.name
        if self.request.GET.get('postCategory') is not None:
            context['category_none']  = True
            context['postCategory'] = Category.objects.filter(id = self.request.GET['postCategory']).first
            # context['postCategorys'] = PostCategory.objects.get(self.request.id) #Post.postCategory.name
            # context['authors'] = Author.objects.all()
            
        return context
    
    def post(self, request, *args, **kwargs):
        # берём значения для нового товара из POST-запроса отправленного на сервер
        PostCategory = request.GET.get('postCategory')
        User = request.user
        subscribe_category = Category.objects.get(id = PostCategory) # создаём новый товар и сохраняем
        subscribe_category.catS_subscribers.add(User)
        subscribe_category.save()
        return redirect('/news')# отправляем пользователя обратно на GET-запрос.
    


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
    


    
    # def get_dropdown(self,request):
    #     if request.method == 'POST':
    #         category_form = PostForm(category_form = request.POST)
    #         if category_form.is_valid():
    #             cdata = category_form.cleaned_data.get
    #         selected_category = request.GET['dropdown']
    #         return selected_category


class PostAdd(PermissionRequiredMixin, CreateView):
    template_name = 'add_news.html'

    form_class = PostForm
    permission_required = 'news.add_news'
    raise_exception = True


    def has_permission(self):
        user_is_author = self.request.user.groups.filter(name = 'authors').exists()
        return user_is_author

    def new_post_to_mail(self, post):
        pass

    
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

 

#B представлении мы добавляем миксин PermissionRequiredMixin:


# class MyView(PermissionRequiredMixin, View):
#     permission_required = ('news.add_news','news.post_delete', 'news.post_update')


# class AddProduct(PermissionRequiredMixin, CreateView):
#     permission_required = ('news.add_news', 'news.post_delete', 'news.post_update')
#     #customize form view


