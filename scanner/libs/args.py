import ast
import argparse

from scanner.utils import std_url


def _set_port_args(parser):
    """Port scan arguments"""

    ports = parser.add_mutually_exclusive_group(required=True)
    ports.add_argument('-p', '--ports', dest='ports',
                       help='Target ports (eg: 80,443,445...)')
    ports.add_argument('--port-file', dest='port_file',
                       help='Port file')

    hosts = parser.add_mutually_exclusive_group(required=True)
    hosts.add_argument('-t', '--hosts', dest='hosts',
                       help='Target hosts (eg: 192.168.1.1/24,192.168.2.1)')
    hosts.add_argument('--host-file', dest='host_file',
                       help='Host file')

    output = parser.add_argument_group('output')
    output.add_argument('-o', '--output', dest='output', default='',
                        help='Save result to a json file')
    output.add_argument('--db', dest='db', action='store_true', default=False,
                        help='Save to MongoDB in config.py')


def _set_vuln_args(parser):
    """Vuln scan args"""

    url = parser.add_mutually_exclusive_group(required=True)
    url.add_argument('-u', '--url', dest='url',
                     help='Target URL')
    url.add_argument('-f', '--file', dest='url_file',
                     help='URL file')

    plugin = parser.add_mutually_exclusive_group(required=True)
    plugin.add_argument('-p', '--plugin', dest='plugin',
                        help='Plugin file')
    plugin.add_argument('-d', '--directory', dest='plugin_directory', default='./plugins',
                        help='Load plugins from a directory')

    request = parser.add_argument_group('request')
    request.add_argument('--cookies', dest='cookies',
                         help='HTTP cookies (eg: "{\'PHPSESSIONID\': \'admin\'}")')
    request.add_argument('--user-agent', dest='user_agent',
                         help='HTTP User-Agent header value')
    request.add_argument('--random-agent', dest='random_agent', action='store_true', default=False,
                         help='Use randomly selected HTTP User-Agent header value')
    request.add_argument('--proxy', dest='proxy',
                         help='Use a proxy to connect to the target URL')
    request.add_argument('--threads', dest='threads', default=5,
                         help='Max number of concurrent HTTP(s) requests (default 5)')

    extra_params = parser.add_argument_group('extra_params')
    extra_params.add_argument('--extra-params', dest='extra_params',
                              help='Extra params for plugins (eg: "{\'user\':\'xxx\', \'pass\':\'xxx\'}")')

    output = parser.add_argument_group('output')
    output.add_argument('-o', '--output', dest='output', default='',
                        help='Save result to a json file')
    output.add_argument('--db', dest='db', action='store_true', default=False,
                        help='Save to MongoDB in config.py')


def _set_sens_args(parser):
    """Sens scan args"""

    url = parser.add_mutually_exclusive_group(required=True)
    url.add_argument('-u', '--url', dest='url',
                     help='Target URL')
    url.add_argument('-f', '--file', dest='url_file',
                     help='URL file')

    wordlist = parser.add_mutually_exclusive_group(required=True)
    wordlist.add_argument('-w', '--wordlist', dest='wordlist',
                          help='Wordlist') 

    request = parser.add_argument_group('request')
    request.add_argument('--cookies', dest='cookies',
                         help='HTTP cookies (eg: "{\'PHPSESSIONID\': \'admin\'}")')
    request.add_argument('--user-agent', dest='user_agent',
                         help='HTTP User-Agent header value')
    request.add_argument('--random-agent', dest='random_agent', action='store_true', default=False,
                         help='Use randomly selected HTTP User-Agent header value')
    request.add_argument('--proxy', dest='proxy',
                         help='Use a proxy to connect to the target URL')
    request.add_argument('--threads', dest='threads', default=5,
                         help='Max number of concurrent HTTP(s) requests (default 5)')
    request.add_argument('--timeout', dest='timeout', default=8,
                         help='Request timeout')

    output = parser.add_argument_group('output')
    output.add_argument('-o', '--output', dest='output', default='',
                        help='Save result to a json file')
    output.add_argument('--db', dest='db', action='store_true', default=False,
                        help='Save to MongoDB in config.py')

def parse_cmd_options():
    """Parse the command line parameters."""

    parser = argparse.ArgumentParser(description=
                                     'My vulnerability testing framework.')

    pattern = parser.add_subparsers(dest='pattern', help='Choose scan pattern')

    port = pattern.add_parser('port', description='Port scan via Masscan',
                              help='Port scan via Masscan')
    vuln = pattern.add_parser('vuln', description='Vulnerability scan via plugins',
                              help='Vulnerability scan via plugins')
    sens = pattern.add_parser('sens', description='Sensitive dir/file scan',
                              help='Sensitive dir/file scan')

    _set_port_args(port)

    _set_vuln_args(vuln)

    _set_sens_args(sens)

    args = parser.parse_args()

    if args.pattern == 'vuln':
        for attr in ['cookies', 'extra_params']:
            if getattr(args, attr):
                setattr(args, attr, ast.literal_eval(getattr(args, attr)))

    if hasattr(args, 'url'):
        urls = []

        if args.url:
            urls.append(std_url(args.url))
        else:
            with open(args.url_file, 'r') as f:
                for url in f:
                    urls.append(std_url(url.strip()))
            urls = list(set(urls))

        args.url = urls

    return args
