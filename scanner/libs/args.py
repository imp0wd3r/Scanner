import ast
import argparse


def parse_cmd_options():
    """Parse the command line parameters."""

    parser = argparse.ArgumentParser(description=
                                     'My vulnerability testing framework.')

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
    request.add_argument('--threads', dest='threads',
                         help='Max number of concurrent HTTP(s) requests (default 5)')

    output = parser.add_argument_group('output')
    output.add_argument('-o', '--output', dest='output', default='/tmp/result.json',
                        help='Save result to a json file')

    extra_params = parser.add_argument_group('extra_params')
    extra_params.add_argument('--extra-params', dest='extra_params',
                              help='Extra params for plugins (eg: "{\'user\':\'xxx\', \'pass\':\'xxx\'}")')

    args = parser.parse_args()

    for attr in ['cookies', 'extra_params']:
        if getattr(args, attr):
            setattr(args, attr, ast.literal_eval(getattr(args, attr)))

    return args
