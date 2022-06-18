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