NewsPaper project - creating application models
 
Comprises:
1 Author model
A model containing objects from all authors.
Has the following fields:
one-to-one relationship with the built-in user model User;
user rating
2 Model Category
Categories of news/articles - the topics they reflect. Has a single field: category name. The field is unique.
3 Post model
This model contains articles and news that users create.
the model includes the following fields:
a one-to-many relationship with the Author model;
a field with a choice - "article" or "news";
automatically added date and time of creation;
a many-to-many relationship with the Category model (with an additional PostCategory model);
article/news title;
the text of the article/news;
article/news rating.
4 PostCategory model
An intermediate model for a many-to-many relationship:
one-to-many relationship with the Post model;
a one-to-many relationship with the Category model.
5 Comment Model
Under each news / article, you can leave comments that are saved.
The model has the following fields:
one-to-many relationship with the Post model;
one-to-many relationship with the built-in User model (any user can leave comments, not necessarily the author);
comment text;
date and time the comment was created;
comment rating.
 
These models also implement methods:
 
The like() and dislike() methods in the Comment and Post models that increase/decrease the rating by one.
The preview() method of the Post model, which returns the beginning of the article (preview) with a length of 124 characters and adds an ellipsis at the end.
The update_rating() method of the Author model, which updates the user's rating passed as an argument to this method.
It consists of the following:
the total rating of each article of the author is multiplied by 3;
total rating of all comments of the author;
the total rating of all comments on the author's articles.
 
The result of the task is prepared in a file ('/NewsPaper/commands.py'), in the form of a list of all commands run in the Django shell.
 
Used commands in Django console:
 
Creating 3 users (using the User.objects.create_user method).
Create 3 Author model objects associated with users.
Adding 4 categories to the Category model.
Adding 2 articles and 1 news.
Category assignment.
Creation of 4 comments to different Post model objects.
The like() and dislike() functions are also applied to articles/news and comments, the ratings of these objects are adjusted.
User rating update.
Output username and rating of the best user using sorting and returning the field of the first object.
Display date added, author's username, rating, title and preview of the best article based on likes/dislikes for this article.
Display all comments (date, user, rating, text) for this article.


The new address page / news /, which contains a list of all news.

All states listed in the type of match, data and the first 50 characters of the text state.
The news is in line with the fresh freshness itself. All news / news / are displayed.

Developed country page / news / <news id>. On this page, all information about the state. Name, text and date of entry in the format DAY-MESY-GOD LAS: MINUTES.

Written by Censor, a filter that cites unhealthy sex in names and text states.
