from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache

class Author(models.Model):
    authors = models.OneToOneField(User, on_delete=models.CASCADE)
    rateAuthor = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.authors.username}'

    def update_rating(self):
        postRate = self.post_set.all().aggregate(postRates=Sum('postRate'))  
        _postRate = 0
        _postRate += postRate.get('postRates')

        commRate = self.authors.comment_set.all().aggregate(commRates=Sum('rateComment')) 
        _commRate = 0
        _commRate += commRate.get('commRates')

        self.rateAuthor = _postRate *3 + _commRate
        self.save()








class Category(models.Model):
    catName = models.CharField(max_length=255, unique=True)
    catS_subscribers = models.ManyToManyField(User, through='SubsCategory') #Для соединения Категории и её подписчиков нарешали мост SubsCategory
    
    def __str__(self):
        return f'{self.catName}'










  #user_posts = Post.objects.filter(created_at__gte = date.today()-timedelta(days=7))
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'

    CATEGORY_CHOICES = (
        (NEWS, 'News'),
        (ARTICLE, 'Article'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    category =  models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS, verbose_name='TypeNews')
    title = models.CharField(max_length=100)
    content = models.TextField(default='content')
    postRate = models.FloatField(default=0.0)


    def __str__(self):
        return '%s %s %s %s %s %s' % (self.created_at, self.author.authors.username, self.author.rateAuthor, self.title, self.content, self.preview())
    
    # допишем свойство, которое будет отображать есть ли товар на складе
    @property
    def rate_plus(self):
        return self.postRate > 0
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'/news/{self.pk}') # затем удаляем его из кэша, чтобы сбросить его
    
    def like(self):
        self.postRate += 1
        self.save()

    def dislike(self):
        self.postRate -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...'

    def get_absolute_url(self):  # aбсолютный путь для перенаправления запроса
        return f'/news/{self.id}' 
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commAuthor = models.ForeignKey(User,default='Guest ', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rateComment = models.FloatField(default=0.0)
    

    def __str__(self):
        try:
            return self.commentPost.author.authorUser.username 
        except:
            return self.commentUser.username 
            
    def __str__(self):
        return self.content

    def like(self):
        self.rateComment += 1
        self.save()
        
    def dislike(self):
        self.rateComment -= 1
        self.save()
    def preview(self):
        return self.content[:124] + '...'

    def get_absolute_url(self):  # aбсолютный путь для перенаправления запроса
        return f'/news/{self.id}'



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.category.catName

class SubsCategory(models.Model): # Мост соеденяющий Категорию и подписоту на эту категорию
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscribers = models.ForeignKey(User, on_delete=models.CASCADE)



class SubscribersMail(models.Model): # модель записи - сообщение от пользователя, его имя и дата записи
    client_title = models.CharField(max_length=200)
    message = models.TextField(default='message_none')
    category = models.TextField(default='category_none')
    subscriber = models.TextField(default='subscriber_none')
    subscriber_email = models.TextField(default='support@gmail.com')
    href = models.TextField(default='')
    def __str__(self):
        return f'{self.client_title}: {self.message}'