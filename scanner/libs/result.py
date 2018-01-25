import os
import json
import inspect
from pprint import pformat

import prettytable
from pymongo import MongoClient
from pymongo.errors import PyMongoError

import config
from scanner.libs.log import logger


def _set_port_table(result):
    table = prettytable.PrettyTable(['host', 'port', 'name', 'product', 'cpe'])

    if not result:
        table.add_row(['All targets', 'No open ports found', '', '', ''])
        logger.info('Here is the result: ')
        print(table)
        os._exit(1)

    result = sorted(result, key=lambda x: x['host'])
    
    for data in result:
        table.add_row([data['host'], data['port'], data['name'], data['product'], data['cpe']])

    return table


def _set_vuln_table(result):
    table = prettytable.PrettyTable(['URL', 'plugin', 'success'])

    for data in result:
        table.add_row([data['url'], data['plugin'], data['success']])
        if data['success'] != 'Exception':
            data['success'] = int(data['success'])

    return table


def _set_sens_table(result):
    table = prettytable.PrettyTable(['URL', 'sensitive', 'status', 'length', 'redirect'])
    if not result:
        table.add_row(['All targets', 'No sensitive dir/file found', '', '', ''])
        logger.info('Here is the result: ')
        print(table)
        os._exit(1)

    result = sorted(result, key=lambda x: x['url'])

    for data in result:
        redirect = '' if not data.setdefault('redirect') else data['redirect']
        table.add_row([data['url'], data['sens'], data['status'], data['len'], redirect])
    
    return table


def save_result(pattern, result, output='', db=False):
    """Save the result."""

    if pattern == 'port':
        table = _set_port_table(result)
    elif pattern == 'vuln':
        table = _set_vuln_table(result)
    else:
        table = _set_sens_table(result)
        
    logger.info('Here is the result: ')
    print(table)
    
    if output:
        with open(output, 'w') as f:
            json.dump(result, f, default=str)

    if db:
        try:
            mongo_client = MongoClient(config.MONGODB_URI)
            db = mongo_client[config.MONGODB_DATABASE] 

            if pattern == 'port':
                collection = db[config.MONGODB_PORT_COLLECTION]
            elif pattern == 'vuln':
                collection = db[config.MONGODB_VULN_COLLECTION]
            else:
                collection = db[config.MONGODB_SENS_COLLECTION]

            for data in result:
                if pattern == 'port':
                    query = {'host': data['host'], 'port': data['port']}
                elif pattern == 'vuln':
                    query = {'url': data['url'], 'plugin': data['plugin']}
                else:
                    query = {'url': data['url'], 'sens': data['sens']}

                collection.update(query, data, upsert=True)

        except PyMongoError as e:
            logger.failure('Failed to save to database\n{}'.format(e))
            os._exit(1)


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
