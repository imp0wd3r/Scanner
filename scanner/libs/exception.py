import os

from scanner.libs.log import logger


def exception_handler(func, url, params):
    """Exception handler for the poc."""

    result = {}

    try:
        result = func(url, params)
    except Exception as e:
        plugin_name = func.__code__.co_filename.replace('plugins/', '')
        logger.failure('Error: {}\n{}\n'.format(plugin_name, e))
        result.update({'url': url, 'plugin': os.path.splitext(os.path.basename(plugin_name))[0], 'success': 'Exception'})

    return result
