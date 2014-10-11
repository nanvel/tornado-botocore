import logging

__version__ = '0.1.4'

try:
    from .base import Botocore
except ImportError:
    logging.warning('Looks like some requirements are missed.')
