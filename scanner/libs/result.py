import os
import sys
import json
import inspect
from pprint import pformat

import prettytable
from pymongo import MongoClient
from pymongo.errors import PyMongoError

import config
from scanner.libs.log import logger


def save_result(pattern, result, output='', db=False):
    """Save the result."""

    if pattern == 'vuln':
        # Vuln scan result
        table = prettytable.PrettyTable(['URL', 'plugin', 'success'])

        for data in result:
            if data:
                table.add_row([data['url'], data['plugin'], data['success']])
                if data['success'] != 'Exception':
                    data['success'] = int(data['success'])
        
        db_result = result
    else:
        # Port scan result
        table = prettytable.PrettyTable(['host', 'ports_open'])

        if not result:
            table.add_row(['All targets', 'No open ports found'])
            logger.info('Here is the result: ')
            print table
            return

        db_result = []

        for host, ports in result.iteritems():
            db_result.append({
                'host': host,
                'ports': ports 
            })
            ports = list(set(ports))
            ports.sort(key=int)
            ports_str = ','.join(ports)
            table.add_row([host, ports_str])
        
    logger.info('Here is the result: ')
    print table
    
    if output:
        with open(output, 'w') as f:
            json.dump(result, f, default=str)

    if db:
        try:
            mongo_client = MongoClient(config.MONGODB_URI)
            db = mongo_client[config.MONGODB_DATABASE] 

            if pattern == 'vuln':
                collection = db[config.MONGODB_VULN_COLLECTION]
            else:
                collection = db[config.MONGODB_PORT_COLLECTION]

            for data in db_result:
                if pattern == 'vuln':
                    query = {'url': data['url'], 'plugin': data['plugin']}
                else:
                    query = {'host': data['host']}
                collection.update(query, data, upsert=True)

        except PyMongoError, e:
            logger.failure('Failed to save to database\n{}'.format(e))
            sys.exit(1)


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
