from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

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

    def __str__(self):
        return self.catName

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    commAuthor = models.ForeignKey(User,default='Anonymus', on_delete=models.CASCADE)
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
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.category

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    


    CATEGORY_CHOICES = (
        (NEWS, 'News'),
        (ARTICLE, 'Article'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    category =  models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS, verbose_name='TypeNews')
    postCategory = models.ManyToManyField(Category, through='PostCategory', verbose_name='Category')
    title = models.CharField(max_length=100)
    content = models.TextField(default='content')
    postRate = models.FloatField(default=0.0)
 

    def __str__(self):
        return self.title +'.'+ '\n' + self.content + '\n'
    

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
    
