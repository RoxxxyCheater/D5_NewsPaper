# from dataclasses import field
# from pyexpat import model #Oxxxy know this!
from django.forms import ModelForm, BooleanField
from .models import Post
 
 
# Создаём модельную форму
class PostForm(ModelForm):
    check_box = BooleanField(label='Я ознакомлен в полном обьёме с правилами ресурса, относительно публикаций и обработки персональных данных авторов статей. Данным действием Соглашаюсь с правилами ресурса.')  #добавляем галочку или же true-false поле , 'check_box'
    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['author','category', 'title','postRate', 'content', 'check_box']
        
