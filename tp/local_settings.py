DEBUG = True

ALLOWED_HOSTS = []

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
STATIC_ROOT = os.path.join(BASE_DIR, 'media')
