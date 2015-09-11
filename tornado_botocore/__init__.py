import logging

__version__ = '1.0.1'

try:
    from .base import Botocore
except ImportError:
    logging.warning('It looks like some requirements are missing.')
