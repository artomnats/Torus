try:
    import sys
    from datetime import timedelta, time
    from os import environ, path, getenv
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(0)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get('SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = environ.get('DEBUG', False)
THUMBNAIL_DEBUG = DEBUG

ALLOWED_HOSTS = [environ.get('DOMAIN', '*')]


DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': environ.get('DB_DATABASE'),
            'USER': environ.get('DB_USERNAME'),
            'PASSWORD': environ.get('DB_PASSWORD'),
            'HOST': environ.get('DB_HOST'),
            'PORT': environ.get('DB_PORT'),
            }
        }

STORAGE_PATHS = {}

STORAGE_PATHS['BASE'] = ''
STORAGE_PATHS['IMAGES'] = path.join(STORAGE_PATHS['BASE'], 'images')
STORAGE_PATHS['FILES'] = path.join(STORAGE_PATHS['BASE'], 'files')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_swagger',
    #'rest_framework_jwt',
    'corsheaders',

    'api',
    'users',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'torus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'torus.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
#TIME_ZONE = 'Australia/Melbourne'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'api.exceptions.custom_exception_handler',
    'AUTH_HEADER_TYPES': 'Bearer',
    'NON_FIELD_ERRORS_KEY': 'object_error',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}

FILE_UPLOAD_MAX_MEMORY_SIZE = 33554432  # 100mb
DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000  # 500mb

# Create AWS configuration
AWS_S3_ACCESS_KEY_ID = environ.get('S3_KEY')
AWS_S3_SECRET_ACCESS_KEY = environ.get('S3_SECRET')
AWS_STORAGE_BUCKET_NAME = environ.get('S3_BUCKET')
AWS_S3_REGION = environ.get('S3_REGION')
AWS_LOCATION = environ.get('AWS_LOCATION', 'static')
AWS_DEFAULT_ACL = environ.get('AWS_DEFAULT_ACL', 'public-read')
# Cause Python does not parse environment variables to Python objects, it just gets them as strings
_AWS_QUERYSTRING_AUTH = environ.get('AWS_QUERYSTRING_AUTH')
AWS_QUERYSTRING_AUTH = _AWS_QUERYSTRING_AUTH if _AWS_QUERYSTRING_AUTH else False
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_HOST = environ.get('AWS_HOST')
AWS_S3_PORT = environ.get('AWS_PORT')
AWS_S3_SENDER = environ.get('AWS_SENDER')
AWS_S3_SENDERNAME = environ.get('AWS_SENDERNAME')
SMTP_USERNAME = environ.get('SMTP_USERNAME')
SMTP_PASSWORD = environ.get('SMTP_PASSWORD')

# Youtube api key
youtube_api_key = environ.get('YOUTUBE_API_KEY')

# STATIC/MEDIA FILES MANAGMENT
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'torus.custom_storages.MediaStorage'

#ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

STATIC_URL = '/static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

try:
    from .local_settings import *
except ImportError:
    try:
        from local_settings import *
    except ImportError:
        print('Local settings couldn\'t be imported.')
