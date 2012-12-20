import os
import sys

import logging

#create logger
logger = logging.getLogger("wsgi")

logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("c:/WSGI.log")
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

fh.setFormatter(formatter)
logger.addHandler(fh)
logger.debug(sys.path)
sys.path.append('d:\\eclipse\\workspace')
sys.path.append('d:\\eclipse\\workspace\\nes_web')
sys.path.append('d:\\eclipse\\workspace\\nes_web\\src')
sys.path.append('d:\\eclipse\\workspace\\nes_web\\src\\nes_phone')
sys.path.append('d:\\virtualenv\\Lib\\site-packages')

logger.debug("final---->>> ")
logger.debug(sys.path)


os.environ['DJANGO_SETTINGS_MODULE'] = 'nes_phone.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()