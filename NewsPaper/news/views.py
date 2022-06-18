from django.shortcuts import render
from django.views.generic import ListView, DetailView,CreateView,UpdateView, DeleteView # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.core.paginator import Paginator # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin #проверка используется для того, чтобы разрешить доступ к странице, которая доступна только для зарегистрированных пользователей.
from .models import Post,Author
from datetime import datetime
from django.views import View # импортируем простую вьюшку
from .filters import NewsFilter # импортируем фильтр
from .forms import PostForm # импортируем форму

 
 
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
        # context['category'] = Post.category
        # context['authors'] = Author.objects.all()
        return context

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST) # создаём новую форму, забиваем в неё данные из POST-запроса 
    #     print(form)
    #     if form.is_valid(): # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
    #         form.save()
 
    #     return super().get(request, *args, **kwargs)
    # def post(self, request, *args, **kwargs):
    #     # берём значения для нового товара из POST-запроса отправленного на сервер
    #     author = request.POST.get('authors') # Author = request.POST['authors']
    #     title= request.POST.get('title')
    #     postRate = request.POST['postRate'] 
    #     content = request.POST.get('content')
    #     posts = Post(author = author, title=title, postRate=postRate, content =content) # создаём новый товар и сохраняем
        
    #     posts.save()
    #     return super().get(request, *args, **kwargs) # отправляем пользователя обратно на GET-запрос.
    
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


class PostAdd(CreateView):
    template_name = 'add_news.html'
    form_class = PostForm

# дженерик для редактирования объекта
class PostUpdateView(UpdateView):
    template_name = 'post_update.html'
    form_class = PostForm
 
    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
 
 
# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
 
 