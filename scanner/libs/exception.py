import os

from scanner.libs.log import logger


def exception_handler(pattern, func, url, params):
    """Exception handler"""

    result = {}

    try:
        result = func(url, params)
    except Exception as e:
        file_name = os.path.splitext(os.path.basename(func.__code__.co_filename))[0]
        if pattern == 'vuln':
            result.update({'url': url, 'plugin': file_name, 'success': 'Exception'})

        logger.failure('Error: {}\n{}\n'.format(file_name, e))

    return result
