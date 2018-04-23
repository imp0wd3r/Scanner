import os
import subprocess
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

import nmap

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

        try:
            _, stderr = process.communicate()
            if not stderr.startswith(b'\nStarting masscan'):
                logger.failure('Masscan Error\n{}'.format(stderr))
                os._exit(1)
        except KeyboardInterrupt:
            logger.failure('User aborted')
            os._exit(1)

    def parse_result_xml(self):
        result = {}
        try:
            tree = ET.parse(self.result_xml)
            root = tree.getroot()

            for host in root.iter('host'):
                ip = host.find('address').attrib['addr']
                port = host.find('ports').find('port').attrib['portid']
                if result.setdefault(ip):
                    result[ip].append(port)
                else:
                    result[ip] = [port]
        except ParseError:
            pass

        return result


class Nmap(object):
    def __init__(self, masscan_result):
        self.nm = nmap.PortScanner(nmap_search_path=(config.NMAP_BIN,))
        self.nmap_args = config.NMAP_ARGS
        self.targets = []
        self.result = []

        for host, ports in masscan_result.items():
            self.targets.append({host: ','.join(ports)})

    def scan(self):
        for target in self.targets:
            for host, ports in target.items():
                self.nm.scan(host, ports, self.nmap_args)

                if host not in self.nm.all_hosts():
                    continue

                if self.nm[host].setdefault('tcp'):
                    for port, data in self.nm[host]['tcp'].items():
                        self.result.append({
                            'host': host,
                            'port': str(port),
                            'name': data['name'],
                            'product': data['product'],
                            'cpe': data['cpe'][7:]
                        })

                if self.nm[host].setdefault('udp'):
                    for port, data in self.nm[host]['udp'].items():
                        self.result.append({
                            'host': host,
                            'port': 'U:{}'.format(port),
                            'name': data['name'],
                            'product': data['product'],
                            'cpe': data['cpe'][7:]
                        })

        return self.result
