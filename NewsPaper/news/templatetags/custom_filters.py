from django import template
 
register = template.Library() # если мы не зарегестрируем наши фильтры, то django никогда не узнает где именно их искать и фильтры потеряются :(


 
 
@register.filter(name='multiply')  
def multiply(value, arg):
    if isinstance(value, str) and isinstance(arg, int): # проверяем, что value — это точно строка, а arg — точно число, чтобы не возникло курьёзов
        return str(value) * arg
    else:
        raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}') # в случае, если кто-то неправильно воспользовался нашим тегом, выводим ошибку

STOP_LIST = [
    'мат',
    'dirty_word',
    'mate',
]

@register.filter(name='Censor') 
def Censor(value, arg):
    for word in value.split():
        if word in STOP_LIST:
           value = value.replace(word, arg)
    return value


    
#     Ban_List = [    
#         "Новости",
#         "lorem",
#         "ipsum"
#     ]
   
# return ' '.join('*'*len(i) if i.upper() in list(map(lambda x: x.upper(), Ban_List)) else i for i in value.split())



# для создания собственных фильтров мы должны сделать следующие шаги:

#     В приложении проекта должны создать директорию templatetags.
#     Добавить в ней пустой файл __init__.py.
#     Создать файл, например, custom_extras.py.
#     В шаблоне прописать {% load custom_extras %}

# В самом файле custom_extras.py необходимо импортировать библиотеку шаблонов:

# from django import template

# register = template.Library()

# Объект register содержит декораторы, благодаря которым можно оборачивать функции в фильтры или тэги. Например, рассмотренный нами фильтр lower будет выглядеть так:

# @register.filter
# def lower(value):
#     return value.lower()

# Для регистрации собственного тэга необходимо использовать другой декоратор simple_tag:

# @register.simple_tag
# def current_time(format_string):
#     return datetime.datetime.now().strftime(format_string)

# Данный тэг вернет текущее время в формате, который передается в качестве аргумента тэга.



forbidden_words = [
    'цензура',
    'свободаслова',
    'демократия'
]


# Реализуйте фильтр, который заменяет все буквы кроме первой и последней на «*» у слов из списка «нежелательных».
# Предполагается, что в качестве аргумента гарантированно передается текст, и слова разделены пробелами.
# Можно считать, что запрещенные слова находятся в списке forbidden_words.


@register.filter(name='multiply')  
def multiply(value, arg):
    words = value.split()
    censored = []
    for word in words:
        if word in forbidden_words:
            censored.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            censored.append(word)
    return " ".join(censored)