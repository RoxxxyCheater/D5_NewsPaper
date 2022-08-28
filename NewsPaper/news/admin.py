from django.contrib import admin
from .models import Comment, Post, Category, SubsCategory
 
# пишем функцию обнуление рейтинга
def nullfy_postRate(modeladmin, request, queryset): # все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(postRate=0)
nullfy_postRate.short_description = 'Обнулить рейтинг' # описание для более понятного представления в админ панеле задаётся, как будто это объект


# создаём новый класс для представления товаров в админке
class PostsAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    #print([field.name for field in Post._meta.get_fields()][1:9]) # генерируем список имён всех полей для более красивого отображения
    list_display = ('id','title','author','category','created_at','postRate','content', 'rate_plus')
    list_filter = ('id','author','category','created_at','postRate') # добавляем примитивные фильтры в нашу админку
    search_fields = ('author','category','content') # тут всё очень похоже на фильтры из запросов в базу, давайте 
    actions = [nullfy_postRate]

admin.site.register(Comment)
admin.site.register(Post, PostsAdmin)
admin.site.register(Category)
admin.site.register(SubsCategory)
#admin.site.unregister(Post) # разрегистрируем наши посты