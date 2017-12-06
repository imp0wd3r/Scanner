import os
import json
import inspect
from pprint import pformat

import prettytable

from scanner.libs.log import logger


def save_result(pattern, result, output='/tmp/result.json'):
    """Save the result."""

    if pattern == 'vuln':
        # Vuln scan result
        table = prettytable.PrettyTable(['URL', 'plugin', 'success'])

        for data in result:
            if data:
                table.add_row([data['url'], data['plugin'], data['success']])
                if data['success'] != 'Exception':
                    data['success'] = int(data['success'])
    else:
        # Port scan result
        table = prettytable.PrettyTable(['host', 'ports_open'])

        for host, ports in result.iteritems():
            if ports == 'No open ports found':
                table.add_row([host, ports])
            else:
                ports = list(set(ports))
                ports.sort(key=int)
                ports_str = ','.join(ports)
                table.add_row([host, ports_str])

    logger.info('Here is the result: ')
    print table

    with open(output, 'w') as f:
        json.dump(result, f, default=str)


def prepare_result(url, success, data={}):
    """Prepare the result via the values that the plugins have returned."""

    plugin = os.path.splitext(os.path.basename(inspect.stack()[1][1]))[0]
    if data:
        if success:
            logger.success('Success! {} -- {}\n{}\n' .format(url, plugin, pformat(data)))
        else:
            logger.failure('Failed. {} -- {}\n{}\n' .format(url, plugin, pformat(data)))
    else:
        if success:
            logger.success('Success! {} -- {}\n' .format(url, plugin))
        else:
            logger.failure('Failed. {} -- {}\n' .format(url, plugin))

    return {'url': url, 'plugin': plugin, 'success': success, 'data': data}
