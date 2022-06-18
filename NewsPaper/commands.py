from NewsPaper.news.models import Author
from news.models import *

############################################################################
#.NewsPaper\Scripts\activate  
############################################################################
#django-admin startproject NewsPaper
############################################################################
#py manage.py help
############################################################################
#cd NewsPaper
############################################################################
#manage.py makemigrations
############################################################################
#python manage.py  migrate
############################################################################
#python manage.py shell
############################################################################
from news.models import *
############################################################################
user1 = User.objects.create(username='Alex')
user2 = User.objects.create(username='Slavik')
user3 = User.objects.create(username='Viktor', first_name='LT')
#>>> print(User.objects.all()) /// Users: <QuerySet [<User: Alex>, <User: Slavik>, <User: Viktor>]>
############################################################################
user1 = User.objects.get(username="Alex")                      
user2 = User.objects.get(username="Slavik")
user3 = User.objects.get(username="Viktor") 
############################################################################
Author.objects.create(authors=user1)
Author.objects.create(authors=user2)
Author.objects.create(authors=user3)
############################################################################
author1 = Author.objects.get(authors = user1.id)
author2 = Author.objects.get(authors = user2.id)
author3 = Author.objects.get(authors = user3.id)
############################################################################
Category.objects.create(catName='Sport')
Category.objects.create(catName='Art')
Category.objects.create(catName='Cinema')
Category.objects.create(catName='IT')
############################################################################
CT1 = Category.objects.get(catName='Sport')
CT2 = Category.objects.get(catName='Art')
CT3 = Category.objects.get(catName='Cinema')
CT4 = Category.objects.get(catName='IT')
Category.objects.all() #<QuerySet [<Category: Sport>, <Category: Art>, <Category: Cinema>, <Category: IT>]>
############################################################################
Post.objects.create(author=author1, category='NW', title='PeaceDeath in all World', text='Rich people make wars in all World - price of Democraty and Capialism')
Post.objects.create(author=author2, category='AR', title='Wild Animals', text='Rich people kills wild Animal for joke or to collects them')
Post.objects.create(author=author3, category='AR', title='Quant Computer', text='With power of Quant PC you can hack everything - and blockchain to')
Post.objects.all().values()
############################################################################
post1 = Post.objects.get(id = 1)
post2 = Post.objects.get(id = 2)
post3 = Post.objects.get(id = 3)
############################################################################
post1.postCategory.add(CT1)
post2.postCategory.add(CT2, CT3)
post3.postCategory.add(CT4, CT1)
############################################################################
Comment.objects.create(commAuthor=user1, commentPost=post1, text='Thats how hell is look like...')
Comment.objects.create(commAuthor=user1, commentPost=post1, text='U right Dude! How to finish this blooding financial games of devil?')
Comment.objects.create(commAuthor=user1, commentPost=post2, text='I belive in carma for this people')
Comment.objects.create(commAuthor=user1, commentPost=post3, text='I belive in carma for <<massons>>')
Comment.objects.all().values() 
############################################################################
com1 = Comment.objects.get(id = 1) 
com2 = Comment.objects.get(id = 2) 
com3 = Comment.objects.get(id = 3) 
com4 = Comment.objects.get(id = 4) 
############################################################################
post1.like()
post1.like()
post2.like()
post3.dislike()
com1.like()
com1.like()
com2.like()
com3.like()
com3.like()
com3.dislike()
##############################################################################
author1.update_rating()
author2.update_rating()
author3.update_rating()
##############################################################################
top_rated = Author.objects.all().order_by('-rateAuthor').values('authors', 'rateAuthor')[0]
print(f'{User.objects.get(id=list(top_rated.values())[0])}: {list(top_rated.values())[1]}')
##############################################################################
bestPost = Post.objects.all().order_by('-postRate').values('created_at', 'author', 'postRate', 'title', 'id')[0]
dateAdd = list(bestPost.values())[0]
author = list(bestPost.values())[1]
username = User.objects.get(id=author)
rating = list(bestPost.values())[2]
title = list(bestPost.values())[3]
postId = list(bestPost.values())[4]
preview = Post.objects.get(title=title, author=author, id = postId).preview()
print(f'{dateAdd}; {username}; {rating}; {title}; {preview}')
##############################################################################
commentsBestPost = Comment.objects.filter(post=postId).values('created_at', 'commAuthor', 'rateComment', 'content')   
print(commentsBestPost.values())
##############################################################################
#python -m pip install django-filter #Не забываем вписать ‘django_filters’ в INSTALLED_APPS в настройках, чтобы получить доступ к фильтрам в приложении.