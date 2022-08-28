from django.core.management.base import BaseCommand, CommandError
from news.models import *

class Command(BaseCommand):
    help = 'удаляет все новости из категории, но только при подтверждении действия в консоли при выполнении команды.'# показывает подсказку при вводе "python manage.py <ваша команда> --help"
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = True # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser): # py manage.py strartproject --template=ARG
        # Positional arguments
        parser.add_argument('argument', type=str)
 
    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнется при вызове вашей команды
        print('It`s working!', options['argument'])
        delcategory = options['argument']
        self.stdout.write(f'Do you really want to clear all posts {delcategory} category? y/n') # спрашиваем пользователя, действительно ли он хочет удалить все товары
        answer =  input() # считываем подтверждение 
        if answer == 'y': # в случае подтверждения действительно удаляем все товары
            #Post.objects.all().delete()
            self.stdout.write('SubsCategory.objects.filter(category = delcategory).objects.all().delete()')
            self.stdout.write(self.style.SUCCESS('Succesfully wiped posts!'))
            return
        self.stdout.write(self.style.ERROR('Access denied')) # в случае неправильного подтверждения, говорим, что в доступе отказано

        # answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')
 
        # if answer != 'yes':
        #     self.stdout.write(self.style.ERROR('Отменено'))
 
        # try:
        #     category = Category.get(name=options['category'])
        #     Post.objects.filter(category==category).delete()
        #     self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.name}')) # в случае неправильного подтверждения говорим, что в доступе отказано
        # except Post.DoesNotExist:
        #     self.stdout.write(self.style.ERROR(f'Could not find category {}'))