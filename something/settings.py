"""
Django settings for something project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""



#############################################

from re import T
from dotenv import load_dotenv
load_dotenv()
import os

################################################



from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY =  str(os.getenv('SECRET_KEY'))
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv('DEBUG'))

BASE_BACKEND_URL = str(os.getenv('BASE_BACKEND_URL'))
BASE_FRONTEND_URL = str(os.getenv('BASE_FRONTEND_URL'))
BASE_FRONTEND_LOGIN_URL = str(os.getenv('BASE_FRONTEND_LOGIN_URL'))

ALLOWED_HOSTS = [
    'somethingnew-testing.herokuapp.com',
    '127.0.0.1',
    'localhost', #set for websocket from reactjs ?
]

# https://pypi.org/project/django-cors-headers/2.5.0/
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#     'http://localhost:3000',
# )

# Application definition

INSTALLED_APPS = [
    'channels', ## this will use ASGI version 3
    # 'daphne', ## this will use ASGI version 4
    # in order to use 'daphne' intead of 'channels' , reinstall the latest pip channels_redis version
    # but there's gonna be some error https://stackoverflow.com/questions/74048946/django-channels-event-loop-is-closing-when-using-thread
    
    # 'rest_framework.authtoken',
    # 'dj_rest_auth',
    # 'dj_rest_auth.registration',
    # 'django.contrib.sites',    
    # 'allauth',    
    # 'allauth.account',    
    # 'allauth.socialaccount',        
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.google',
    'graphene_django',
    'phonenumber_field',
    'marketplace',
    'realtime',
    'app',
    'user',
    'rest_framework',
    'corsheaders',
    'versatileimagefield',
    'storages',
    'django_filters',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

#https://python.plainenglish.io/social-media-rest-authentication-so-easy-that-you-will-laugh-django-7bca6869f931
SITE_ID=1


AUTH_USER_MODEL = 'user.CustomUser'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'user.backends.AuthBackend',
    ] # new

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':(
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_PAGINATION_CLASS':'something.pagination.MycustomPagination',
    'PAGE_SIZE': 5,
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",

    # IF NOT add the filter backend to an individual View or ViewSet, enable this
    # 'DEFAULT_FILTER_BACKENDS': [
    #     'django_filters.rest_framework.DjangoFilterBackend',
    # ],
}

# If we didn’t specify the target schema in the urls.ply, we can do so here using
# GRAPHENE = {
#     "SCHEMA": "marketplace.schema.schema"
# }


from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=3),
}

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",   #whitenoise
    'corsheaders.middleware.CorsMiddleware',    #corsheaders
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'something.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

ASGI_APPLICATION = 'something.asgi.application'
CHANNEL_LAYERS = {
    "default":{
        "BACKEND":"channels_redis.core.RedisChannelLayer",
        # https://stackoverflow.com/questions/74048946/django-channels-event-loop-is-closing-when-using-thread
        # "BACKEND":"channels_redis.pubsub.RedisPubSubChannelLayer",
        # solved by downgrading channels_redis version to 3.3.1
        "CONFIG":{
            "hosts":[("127.0.0.1",6379)],   # currently using docker
        },
    },
}
WSGI_APPLICATION = 'something.wsgi.application'





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

POSTGRES = str(os.getenv('POSTGRES'))

if DEBUG:
# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
    if POSTGRES=="TRUE":
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': str(os.getenv('POSTGRES_DB_NAME')),
                'USER': str(os.getenv('POSTGRES_USER')),
                'PASSWORD': str(os.getenv('POSTGRES_PASSWORD')),
                'HOST': str(os.getenv('POSTGRES_HOST')),
                'PORT': str(os.getenv('POSTGRES_PORT')),
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            # "NAME": config("DB_NAME"),
            # "USER": config("DB_USER"),
            # "PASSWORD": config("DB_PWD"),
            # "HOST": config("DB_HOST"),
            # "PORT": config("DB_PORT"),
        }
    }

USE_S3 = str(os.getenv('USE_S3'))
if USE_S3 == 'TRUE':

    #S3 BUCKETS CONFIG

    # get Access and Secret from IAM user
    AWS_ACCESS_KEY_ID = str(os.getenv('AWS_ACCESS_KEY_ID'))
    AWS_SECRET_ACCESS_KEY = str(os.getenv('AWS_SECRET_ACCESS_KEY'))

    AWS_STORAGE_BUCKET_NAME = str(os.getenv('AWS_STORAGE_BUCKET_NAME'))
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# Enable WhiteNoise's GZip compression of static assets.
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


VERSATILEIMAGEFIELD_SETTINGS = {
    # The amount of time, in seconds, that references to created images
    # should be stored in the cache. Defaults to `2592000` (30 days)
    'cache_length': 2592000,
    # The name of the cache you'd like `django-versatileimagefield` to use.
    # Defaults to 'versatileimagefield_cache'. If no cache exists with the name
    # provided, the 'default' cache will be used instead.
    'cache_name': 'versatileimagefield_cache',
    # The save quality of modified JPEG images. More info here:
    # https://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html#jpeg
    # Defaults to 70
    'jpeg_resize_quality': 70,
    # The name of the top-level folder within storage classes to save all
    # sized images. Defaults to '__sized__'
    'sized_directory_name': '__sized__',
    # The name of the directory to save all filtered images within.
    # Defaults to '__filtered__':
    'filtered_directory_name': '__filtered__',
    # The name of the directory to save placeholder images within.
    # Defaults to '__placeholder__':
    'placeholder_directory_name': '__placeholder__',
    # Whether or not to create new images on-the-fly. Set this to `False` for
    # speedy performance but don't forget to 'pre-warm' to ensure they're
    # created and available at the appropriate URL.
    'create_images_on_demand': True,
    # A dot-notated python path string to a function that processes sized
    # image keys. Typically used to md5-ify the 'image key' portion of the
    # filename, giving each a uniform length.
    # `django-versatileimagefield` ships with two post processors:
    # 1. 'versatileimagefield.processors.md5' Returns a full length (32 char)
    #    md5 hash of `image_key`.
    # 2. 'versatileimagefield.processors.md5_16' Returns the first 16 chars
    #    of the 32 character md5 hash of `image_key`.
    # By default, image_keys are unprocessed. To write your own processor,
    # just define a function (that can be imported from your project's
    # python path) that takes a single argument, `image_key` and returns
    # a string.
    'image_key_post_processor': None,
    # Whether to create progressive JPEGs. Read more about progressive JPEGs
    # here: https://optimus.io/support/progressive-jpeg/
    'progressive_jpeg': False
}

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'image_gallery': [
        ('gallery_large', 'crop__800x450'),
        ('gallery_square_small', 'crop__50x50')
    ],
    'primary_image_detail': [
        ('hero', 'crop__600x283'),
        ('social', 'thumbnail__800x800')
    ],
    'primary_image_list': [
        ('list', 'crop__400x225'),
    ],
    'headshot': [
        ('headshot_small', 'crop__150x175'),
    ]
}

EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = str(os.getenv('EMAIL_HOST_USER'))

EMAIL_HOST_PASSWORD = str(os.getenv('EMAIL_HOST_PASSWORD'))

EMAIL_PORT = 587

# celery
REDIS_HOST = 'localhost' 
REDIS_PORT = '6379' 
BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0' 
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600} 
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'

GOOGLE_OAUTH2_CLIENT_ID = str(os.getenv('GOOGLE_OAUTH2_CLIENT_ID'))
GOOGLE_OAUTH2_CLIENT_SECRET = str(os.getenv('GOOGLE_OAUTH2_CLIENT_SECRET'))


