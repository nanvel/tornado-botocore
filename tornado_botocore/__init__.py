import logging

__version__ = '0.1.5'

try:
    from .base import Botocore
except ImportError:
    logging.warning('It looks like some requirements are missing.')
