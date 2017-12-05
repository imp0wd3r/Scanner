import ast
import argparse


def parse_cmd_options():
    """Parse the command line parameters."""

    parser = argparse.ArgumentParser(description=
                                     'My vulnerability testing framework.')

    pattern = parser.add_subparsers(dest='pattern', help='Choose scan pattern')

    port = pattern.add_parser('port', description='Port scan via Masscan',
                              help='Port scan via Masscan')
    vuln = pattern.add_parser('vuln', description='Vulnerability scan via plugins',
                              help='Vulnerability scan via plugins')

    # Port scan arguments
    ports = port.add_mutually_exclusive_group(required=True)
    ports.add_argument('-p', '--ports', dest='ports',
                       help='Target ports (eg: 80,443,445...)')
    ports.add_argument('--port-file', dest='port_file',
                       help='Port file')

    hosts = port.add_mutually_exclusive_group(required=True)
    hosts.add_argument('-t', '--hosts', dest='hosts',
                       help='Target hosts (eg: 192.168.1.1/24,192.168.2.1)')
    hosts.add_argument('--host-file', dest='host_file',
                       help='Host file')

    # Vuln scan arguments
    url = vuln.add_mutually_exclusive_group(required=True)
    url.add_argument('-u', '--url', dest='url',
                     help='Target URL')
    url.add_argument('-f', '--file', dest='url_file',
                     help='URL file')

    plugin = vuln.add_mutually_exclusive_group(required=True)
    plugin.add_argument('-p', '--plugin', dest='plugin',
                        help='Plugin file')
    plugin.add_argument('-d', '--directory', dest='plugin_directory', default='./plugins',
                        help='Load plugins from a directory')

    request = vuln.add_argument_group('request')
    request.add_argument('--cookies', dest='cookies',
                         help='HTTP cookies (eg: "{\'PHPSESSIONID\': \'admin\'}")')
    request.add_argument('--user-agent', dest='user_agent',
                         help='HTTP User-Agent header value')
    request.add_argument('--random-agent', dest='random_agent', action='store_true', default=False,
                         help='Use randomly selected HTTP User-Agent header value')
    request.add_argument('--proxy', dest='proxy',
                         help='Use a proxy to connect to the target URL')
    request.add_argument('--threads', dest='threads',
                         help='Max number of concurrent HTTP(s) requests (default 5)')

    extra_params = vuln.add_argument_group('extra_params')
    extra_params.add_argument('--extra-params', dest='extra_params',
                              help='Extra params for plugins (eg: "{\'user\':\'xxx\', \'pass\':\'xxx\'}")')

    output = parser.add_argument_group('output')
    output.add_argument('-o', '--output', dest='output', default='/tmp/result.json',
                        help='Save result to a json file')

    args = parser.parse_args()

    if args.pattern == 'vuln':
        for attr in ['cookies', 'extra_params']:
            if getattr(args, attr):
                setattr(args, attr, ast.literal_eval(getattr(args, attr)))

    return args
