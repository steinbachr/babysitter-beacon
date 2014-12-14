"""
Django settings for Babysitter project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'eczxxlstekd_61kvw@yic!o#s!)e2f*x$4z+mj(bz+6cy$dm^w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

LOGIN_URL = '/'
LOGOUT_URL = '/accounts/logout/'

AUTHENTICATION_BACKENDS = (
    'web.authentication.ParentBackend',
    'web.authentication.SitterBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'widget_tweaks',
    'pipeline',
    'rest_framework',
    'api',
    'web'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Babysitter.urls'

WSGI_APPLICATION = 'Babysitter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'dev': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'sitter_dev',
        'USER': 'bobbysteinbach',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
    'prod': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sitter_prod',
        'USER': 'sitter_user',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'web/static/build/')
STATIC_URL = '/static/'


#####-----< Django Pipeline >-----#####
PIPELINE_JS = {
    'core': {
        'source_filenames': (
            'files/js/vendor/jquery.js',
            'files/js/vendor/jquery.easing.min.js',
            'files/js/vendor/bootstrap.js',
            'files/js/vendor/underscore-min.js',
            'files/js/vendor/backbone-min.js',
        ),
        'output_filename': 'build/core.js'
    },
    'index': {
        'source_filenames': (
            'files/js/app/index.js',
        ),
        'output_filename': 'build/index.js'
    },
    'parents': {
        'source_filenames': (
            'files/js/app/parents/models/Child.js',
            'files/js/app/parents/models/Parent.js',
            'files/js/app/parents/parents.js',
        ),
        'output_filename': 'build/parents.js'
    }
}

PIPELINE_CSS = {
    'core': {
        'source_filenames': (
            'files/css/vendor/bootstrap.css',
            'files/css/vendor/font-awesome/css/font-awesome.min.css',
            'files/css/app/core.less',
        ),
        'output_filename': 'build/core.css'
    },
    'index': {
        'source_filenames': (
            'files/css/app/index.less',
        ),
        'output_filename': 'build/index.css'
    },
    'signup': {
        'source_filenames': (
            'files/css/app/signup.less',
        ),
        'output_filename': 'build/signup.css'
    },
    'parents': {
        'source_filenames': (
            'files/css/app/parents.less',
        ),
        'output_filename': 'build/parents.css'
    }
}

PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_TEMPLATE_FUNC = '_.template'

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)


#####-----< Switches >-----#####
if DEBUG:
    DATABASES['default'] = DATABASES['dev']
else:
    DATABASES['default'] = DATABASES['prod']

if DEBUG:
    DOMAIN = "0.0.0.0:8000"
