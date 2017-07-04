import dj_database_url
from blogIT.settings.common import *

DEBUG = False


DATABASES = {
    'default': dj_database_url.config()
}
