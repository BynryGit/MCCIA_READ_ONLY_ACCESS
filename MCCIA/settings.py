"""
Django settings for MCCIA project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import logging, logging.config
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j3q9o&ig-$pxl96^-e^3&$)jwyr$!yyx(h2j!m7o_=@#-8d-7q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'backofficeapp',
    'adminapp',
    'membershipapp',
    'hallbookingapp',
    # 'awardsapp',
    'eventsapp',
    # 'publicationapp',

    'backofficeapp.templatetags.my_template_tag',
    'django_crontab',
    'Paymentapp',
    'visarecommendationapp',
    'initiativesapp',
    'mediaapp',
    'publicationapp',
    'massmailingapp',
    'reportapp',
    'wkhtmltopdf',
    'awardsapp',
    'sustainabilityapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'MCCIA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MCCIA.wsgi.application'


#Database
#https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': "mccia_backoffice",
#         'USER':'mcciamaster',
#         'PASSWORD':'mccia2018',
#         'HOST':'mcciards.cgpq7jl3q6df.ap-south-1.rds.amazonaws.com',
#         'PORT':'3306',
#         'TIME_ZONE': 'Asia/Kolkata',
#      }
# }

DATABASES = {
  'default': {
      'ENGINE': 'django.db.backends.mysql',
      'NAME': "mccia_backoffice",
      'USER':'root',
      'PASSWORD':'root',
      'HOST':'localhost',
      'PORT':'3306',
      'TIME_ZONE': 'Asia/Kolkata',
  }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR + '/site-static/'
STATICFILES_DIRS = (BASE_DIR + '/site-static/',)
# STATIC_ROOT = os.path.join(BASE_DIR, 'site-static')

MEDIA_ROOT = BASE_DIR + '/sitemedia/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://example.com/media/"
MEDIA_URL = '/sitemedia/'


#GOOGLE_RECAPTCHA_SECRET_KEY = '6Lf0Gl4UAAAAALw9xU-uY0xQpceB-xSULFYFzdRc'


#SITE_KEY = "6Lf0Gl4UAAAAAIjC0zhqURboCEzC0pPjdqSZmD7e"


#### for AWS server --------------

GOOGLE_RECAPTCHA_SECRET_KEY = '6LcPTV0UAAAAAHcWQgytDV7XurRCbx7rXedKP9cQ'


SITE_KEY = "6LcPTV0UAAAAAHlTBrvPhN4oCSqDPDoWpLk70l3d"

### CRON JOB
CRONJOBS = [
    # ('* * * * *', 'eventsapp.view.cron_job.update_event_view_status','>> '+BASE_DIR+'/tmp/scheduled_job.log 2>&1'),
    # ('*/30 * * * *', 'hallbookingapp.view.hall_booking_task.cancel_invalid_booking','>> '+BASE_DIR+'/tmp/hall_booking_scheduled_job.log 2>&1'),
]

# LOGGING = {
#     'version': 1,

#     'handlers': {
#         'console': {
#             'level': 'ERROR',            
#             'class': 'logging.StreamHandler',
#         },     
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'ERROR',
#         },        
#     }
# }

WKHTMLTOPDF_CMD = '/usr/bin/wkhtmltopdf'


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
#         },
#     },
# }

# DJANGO_LOG_LEVEL=DEBUG 

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': ''+BASE_DIR+'/tmp/debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }



# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level':'DEBUG',
#             'class':'logging.StreamHandler'
#         },
#     },
#     'loggers': {
#         '': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + "/logfile",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}
