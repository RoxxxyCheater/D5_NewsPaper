LOGGING = {
    'version': 1, #Идентифицирует конфигурацию как имеющую формат „dictConfig версии 1“.
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': { #выводит имя уровня журнала, сообщение журнала, а также время, процесс, поток и модуль, которые генерируют сообщение журнала.
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': { #simple, который выводит имя уровня журнала (например, DEBUG) и сообщение журнала.
            'format': '{levelname} {message}', #детали, которые должны быть выведены в каждой строке журнала.
            'style': '{',
        },
    },
    'filters': { #Определяет два фильтра,используя псевдоним special.
        'special': {
            '()': 'project.logging.SpecialFilter', #дополнительные аргументы могут быть предоставлены как дополнительные ключи в словаре конфигурации фильтра. 
            'foo': 'bar', #аргументу foo будет присвоено значение bar при инстанцировании SpecialFilter.
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue', #передает записи, когда DEBUG становится True.
        },
    },
    'handlers': {
        'console': { 
            'level': 'INFO', #печатает любое сообщение INFO (или выше) в sys.stderr
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler', #console обработчик
            'formatter': 'simple' #использует формат вывода simple.
        },
        'mail_admins': {
            'level': 'ERROR', # отправляет любое сообщение ERROR (или выше) на сайт ADMINS.
            'class': 'django.utils.log.AdminEmailHandler', #mail_admins обработчик
            'filters': ['special'] # использует фильтр special.
        }
    },
    'loggers': {
        'django': { #регистратор django, который передает все сообщения обработчику console.
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': { #передает все сообщения ERROR обработчику mail_admins
            'handlers': ['mail_admins'], 
            'level': 'ERROR',
            'propagate': False, #не распространяющий сообщения - сообщения журнала, записанные в django.request, не будут обработаны регистратором django. 
        },
        'myproject.custom': { #передает все сообщения уровня INFO или выше, которые также проходят фильтр special, двум обработчикам ниже
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO', #все сообщения уровня INFO (или выше) будут выведены на консоль
            'filters': ['special'] #ERROR и CRITICAL сообщения также будут выведены по электронной почте.
        }
    }
}