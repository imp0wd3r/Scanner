import sys
import subprocess
import xml.etree.ElementTree as ET

import config
from scanner.libs.log import logger


class Masscan(object):
    def __init__(self, args):
        self.masscan_bin = config.MASSCAN_BIN
        self.result_xml = config.MASSCAN_RESULT_XML
        self.rate = config.MASSCAN_RATE
        self.retries = config.MASSCAN_RETRIES
        self.wait = config.MASSCAN_WAIT

        if args.ports:
            self.ports = args.ports
        else:
            with open(args.port_file, 'r') as f:
                self.ports = ','.join([line.strip() for line in f])

        if args.hosts:
            self.hosts = args.hosts
        else:
            with open(args.host_file, 'r') as f:
                self.hosts = ','.join([line.strip() for line in f])

    def scan(self):
        command = (
            '{masscan_bin} -oX {result_xml} --rate={rate} --retries={retries} --wait={wait} -p {ports} {hosts}'
        ).format(
            masscan_bin=self.masscan_bin,
            result_xml=self.result_xml,
            rate=self.rate,
            retries=self.retries,
            wait=self.wait,
            hosts=self.hosts,
            ports=self.ports
        )

        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )

        _, stderr = process.communicate()
        if not stderr.startswith('\nStarting masscan'):
            logger.failure(stderr)
            sys.exit(1)

    def parse_result_xml(self):
        tree = ET.parse(self.result_xml)
        root = tree.getroot()

        result = {}
        for host in root.iter('host'):
            ip = host.find('address').attrib['addr']
            port = host.find('ports').find('port').attrib['portid']
            if result.setdefault(ip):
                result[ip].append(port)
            else:
                result[ip] = [port]
        
        return result
