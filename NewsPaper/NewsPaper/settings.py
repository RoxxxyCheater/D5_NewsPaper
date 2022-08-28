"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""


from pathlib import Path
import os
from Server_auth import SECRET_KEY, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL, EMAIL_HOST_USER

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SECRET_KEY = SECRET_KEY
ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['127.0.0.1']
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions', # Данное приложение выполняет задачу управления сессиями. 
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.google',
    'news',
    'accounts',
    'django_filters', # получить доступ к фильтрам в приложении.
    'sign', #приложение регистрации, аутентификации и авторизации
    'protect', #приложение c представлением для аутентифицированных пользователей. 
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.auth', # поддержка авторизации реализуется в виде приложения, автоматически подключаемого к каждому новому проекту
    'django_apscheduler',
    
    # 'allauth.socialaccount.providers.agave',
    # 'allauth.socialaccount.providers.amazon',
    # 'allauth.socialaccount.providers.amazon_cognito',
    # 'allauth.socialaccount.providers.angellist',
    # 'allauth.socialaccount.providers.apple',
    # 'allauth.socialaccount.providers.asana',
    # 'allauth.socialaccount.providers.auth0',
    # 'allauth.socialaccount.providers.authentiq',
    # 'allauth.socialaccount.providers.azure',
    # 'allauth.socialaccount.providers.baidu',
    # 'allauth.socialaccount.providers.basecamp',
    # 'allauth.socialaccount.providers.battlenet',
    # 'allauth.socialaccount.providers.bitbucket',
    # 'allauth.socialaccount.providers.bitbucket_oauth2',
    # 'allauth.socialaccount.providers.bitly',
    # 'allauth.socialaccount.providers.box',
    # 'allauth.socialaccount.providers.cern',
    # 'allauth.socialaccount.providers.cilogon',
    # 'allauth.socialaccount.providers.clever',
    # 'allauth.socialaccount.providers.coinbase',
    # 'allauth.socialaccount.providers.dataporten',
    # 'allauth.socialaccount.providers.daum',
    # 'allauth.socialaccount.providers.digitalocean',
    # 'allauth.socialaccount.providers.discord',
    # 'allauth.socialaccount.providers.disqus',
    # 'allauth.socialaccount.providers.douban',
    # 'allauth.socialaccount.providers.doximity',
    # 'allauth.socialaccount.providers.draugiem',
    # 'allauth.socialaccount.providers.drip',
    # 'allauth.socialaccount.providers.dropbox',
    # 'allauth.socialaccount.providers.dwolla',
    # 'allauth.socialaccount.providers.edmodo',
    # 'allauth.socialaccount.providers.edx',
    # 'allauth.socialaccount.providers.eventbrite',
    # 'allauth.socialaccount.providers.eveonline',
    # 'allauth.socialaccount.providers.evernote',
    # 'allauth.socialaccount.providers.exist',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.feedly',
    # 'allauth.socialaccount.providers.figma',
    # 'allauth.socialaccount.providers.fivehundredpx',
    # 'allauth.socialaccount.providers.flickr',
    # 'allauth.socialaccount.providers.foursquare',
    # 'allauth.socialaccount.providers.frontier',
    # 'allauth.socialaccount.providers.fxa',
    # 'allauth.socialaccount.providers.gitea',
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.gitlab',
    # 'allauth.socialaccount.providers.globus',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.gumroad',
    # 'allauth.socialaccount.providers.hubic',
    # 'allauth.socialaccount.providers.instagram',
    # 'allauth.socialaccount.providers.jupyterhub',
    # 'allauth.socialaccount.providers.kakao',
    # 'allauth.socialaccount.providers.keycloak',
    # 'allauth.socialaccount.providers.lemonldap',
    # 'allauth.socialaccount.providers.line',
    # 'allauth.socialaccount.providers.linkedin',
    # 'allauth.socialaccount.providers.linkedin_oauth2',
    # 'allauth.socialaccount.providers.mailchimp',
    # 'allauth.socialaccount.providers.mailru',
    # 'allauth.socialaccount.providers.mediawiki',
    # 'allauth.socialaccount.providers.meetup',
    # 'allauth.socialaccount.providers.microsoft',
    # 'allauth.socialaccount.providers.naver',
    # 'allauth.socialaccount.providers.nextcloud',
    # 'allauth.socialaccount.providers.odnoklassniki',
    # 'allauth.socialaccount.providers.openid',
    # 'allauth.socialaccount.providers.openstreetmap',
    # 'allauth.socialaccount.providers.orcid',
    # 'allauth.socialaccount.providers.patreon',
    # 'allauth.socialaccount.providers.paypal',
    # 'allauth.socialaccount.providers.persona',
    # 'allauth.socialaccount.providers.pinterest',
    # 'allauth.socialaccount.providers.pocket',
    # 'allauth.socialaccount.providers.quickbooks',
    # 'allauth.socialaccount.providers.reddit',
    # 'allauth.socialaccount.providers.robinhood',
    # 'allauth.socialaccount.providers.salesforce',
    # 'allauth.socialaccount.providers.sharefile',
    # 'allauth.socialaccount.providers.shopify',
    # 'allauth.socialaccount.providers.slack',
    # 'allauth.socialaccount.providers.snapchat',
    # 'allauth.socialaccount.providers.soundcloud',
    # 'allauth.socialaccount.providers.spotify',
    # 'allauth.socialaccount.providers.stackexchange',
    # 'allauth.socialaccount.providers.steam',
    # 'allauth.socialaccount.providers.stocktwits',
    # 'allauth.socialaccount.providers.strava',
    # 'allauth.socialaccount.providers.stripe',
    # 'allauth.socialaccount.providers.telegram',
    # 'allauth.socialaccount.providers.trainingpeaks',
    # 'allauth.socialaccount.providers.trello',
    # 'allauth.socialaccount.providers.tumblr',
    # 'allauth.socialaccount.providers.twentythreeandme',
    # 'allauth.socialaccount.providers.twitch',
    # 'allauth.socialaccount.providers.twitter',
    # 'allauth.socialaccount.providers.untappd',
    # 'allauth.socialaccount.providers.vimeo',
    # 'allauth.socialaccount.providers.vimeo_oauth2',
    # 'allauth.socialaccount.providers.vk',
    # 'allauth.socialaccount.providers.weibo',
    # 'allauth.socialaccount.providers.weixin',
    # 'allauth.socialaccount.providers.windowslive',
    # 'allauth.socialaccount.providers.xing',
    # 'allauth.socialaccount.providers.yahoo',
    # 'allauth.socialaccount.providers.yandex',
    # 'allauth.socialaccount.providers.ynab',
    # 'allauth.socialaccount.providers.zoho',
    # 'allauth.socialaccount.providers.zoom',
    # 'allauth.socialaccount.providers.okta',
    # 'allauth.socialaccount.providers.feishu',

]

# Format string for displaying run time timestamps in the Django admin site. The default
# just adds seconds to the standard Django format, which is useful for displaying the timestamps
# for jobs that are scheduled to run on intervals of less than one minute.
# 
# See https://docs.djangoproject.com/en/dev/ref/settings/#datetime-format for format string
# syntax details.
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

# Maximum run time allowed for jobs that are triggered manually via the Django admin site, which
# prevents admin site HTTP requests from timing out.
# 
# Longer running jobs should probably be handed over to a background task processing library
# that supports multiple background worker processes instead (e.g. Dramatiq, Celery, Django-RQ,
# etc. See: https://djangopackages.org/grids/g/workers-queues-tasks/ for popular options).
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

SITE_ID = 1 #SITE_ID используется в случае, если данный проект управляет несколькими сайтами, но для нас сейчас это не является принципиальным. Достаточно явно прописать значение 1 для этой переменной.


# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '123',
            'secret': '456',
            'key': ''
        }
    }
}
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 180
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', #Слой безопасности SecurityMiddleware должен находиться как можно выше в списке, чтобы отсеивать запросы, нарушающие безопасность, и не тратить время на их обработку.
    'django.contrib.sessions.middleware.SessionMiddleware', #SessionMiddleware должен вызываться перед слоями, которые связаны с авторизацией, и могут вызвать исключения типа PermissionDenied.
    'django.middleware.common.CommonMiddleware', #CommonMiddleware должен запускаться перед слоями, которые могут изменить ответ на запрос.
    'django.middleware.csrf.CsrfViewMiddleware', #Слои CsrfViewMiddleware, AuthenticationMiddleware, MessageMiddleware должны находиться строго после слоя сессий SessionMiddleware.
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'news.middlewares.ViewVersionMiddleware',
]

    #Кэширующий слой должен находиться до слоев, связанных с сессиями, куки и слоем локализации.
    #LocaleMiddleware также должен находиться как можно выше, но обязательно после кэширующего слоя и слоя сессий.
    




ROOT_URLCONF = 'NewsPaper.urls'

TEMPLATES = [ #контекстный процессор
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #`allauth` needs this from django
                'django.template.context_processors.request'
            ],
        },
    },
]

#Далее нам необходимо добавить бэкенды аутентификации как по username, так и специфичную по email или сервис-провайдеру: 


AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend', # встроенный бэкенд Django, реализующий аутентификацию по username

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend', #бэкенд аутентификации, предоставленный пакетом allauth
]

WSGI_APPLICATION = 'NewsPaper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ACCOUNT_EMAIL_REQUIRED = True #имейл обязательно
ACCOUNT_UNIQUE_EMAIL = True # уникальный имейл
ACCOUNT_USERNAME_REQUIRED = False #username обязательно
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_REDIRECT_URL
ACCOUNT_FORMS = {'signup': 'sign.models.BasicSignupForm'} #allauth распознал нашу форму как ту, что должна выполняться вместо формы по умолчанию.
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True
ACCOUNT_EMAIL_SUBJECT_PREFIX ="[http://127.0.0.1:8000/news/] " 

EMAIL_HOST = 'smtp.gmail.com' # адрес сервера Яндекс-почты для всех один и тот же
EMAIL_PORT = 465 # порт smtp сервера тоже одинаковый
EMAIL_HOST_USER = EMAIL_HOST_USER # ваше имя пользователя, например если ваша почта user@yandex.ru, то сюда надо писать user, иными словами, это всё то что идёт до собаки
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD # пароль от почты
EMAIL_USE_SSL = True # использует ssl, подробнее о том, что это, почитайте на Википедии, но включать его здесь обязательно
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL # здесь указываем уже свою ПОЛНУЮ почту с которой будут отправляться письма 

# # формат даты, которую будет воспринимать наш задачник(вспоминаем урок по фильтрам) 
# APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
 
# # если задача не выполняется за 25 секунд, то она автоматически снимается, можете поставить время побольше, но как правило, это сильно бьёт по производительности сервера
# APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # Указываем, куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': { #записывать информацию согласно определенным форматам.
        'console_form': {
            'format': '***{asctime} {levelname} [{message}]',
            'style': '{'
        },
        'console_form_warn': {
            'format': '***{asctime} {levelname} [{message}] [{pathname}]',
            'style': '{'
        },
        'console_form_error': {
            'format': '***{asctime} {levelname} [{message}] [{pathname}] {exc_info}',
            'style': '{'
        },
        'gen_sec_mail_form': {
            'format': '***{asctime} {levelname} {module} {message}',
            'style': '{'
        },   
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'ERROR', 
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_form_error'
        },
        'console': {
            'level': 'WARNING', 
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_form_warn'
        },
        'console': {
            'level': 'INFO', 
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_form'
        },
        'general_log': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'formatter': 'gen_sec_mail_form',
            'filename': 'NewsPaper/general.log',
        },
        'error_log': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'console_form_error',
            'filename': 'NewsPaper/error.log'
        },
        'security_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'gen_sec_mail_form',
            'filename': 'NewsPaper/security.log' 
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'gen_sec_mail_form'
        }

    },
    'loggers': { 
        'news': {
            'handlers': ['console', 'general_log'],
            'level': 'DEBUG', 
            'propagate': True,
        },
        'django': {
            'handlers': ['console', 'general_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request':{
            'handlers': ['error_log', 'mail_admins'],
            'level': 'ERROR',
        },
        'django.server':{
            'handlers': ['error_log', 'mail_admins'],
            'level': 'ERROR',
        },
        'django.template':{
            'handlers': ['error_log'],
            'level': 'ERROR',
        },
        'django.db_backends': {
            'handlers': ['error_log'],
            'level': 'ERROR',
        },
        'django.security': {
            'handlers': ['security_log'],
            'propagate': False,
        }
    }
}

#+ В консоль должны выводиться все сообщения уровня DEBUG и выше
#+ Формат время, уровень сообщения, сообщения
# Для сообщений WARNING и выше дополнительно должен выводиться путь к источнику события (используется аргумент pathname в форматировании).
# ERROR и CRITICAL еще должен выводить стэк ошибки (аргумент exc_info).
# а должны попадать все сообщения с основного логгера django.


# В файл general.log сообщения уровня INFO и выше + сообщения с регистратора django
# формат времени, уровня логирования, модуля(аргумент module) и сообщение.
# + сообщения с регистратора django


# В файл errors.log только уровня ERROR и CRITICAL.
# формат время, уровень логирования, сообщение, путь к источнику сообщения и стэк ошибки.
# В файл errors.log сообщения только из логгеров django.request, django.server, django.template, django.db_backends.


# В файл security.log сообщения только из логгера django.security.
# Формат:  время, уровень логирования, модуль и сообщение.


# На почту: сообщения уровней ERROR и выше из django.request и django.server,
# формат: время, уровень логирования, модуль и сообщение.
# 
# 
#+ в консоль сообщения о тправляются только при DEBUG = True,
# а на почту и в файл general.log только при DEBUG = False.

