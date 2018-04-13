import socket
from urllib.parse import urlparse

import requests
from netaddr import valid_ipv4

from scanner.libs.result import prepare_result


def poc(url, params):
    hostname = urlparse(url).hostname
    if valid_ipv4(hostname):
        ip = hostname
    else:
        ip = socket.gethostbyname(hostname)

    headers = {'User-Agent': 'curl/7.55.1'}
    u = 'http://ipinfo.io/{}'.format(ip)
    rep = requests.get(u, timeout=10, headers=headers)
    if rep.status_code == 200:
        return prepare_result(url, True, rep.json())
    else:
        return prepare_result(url, False, {'msg': rep.content})
