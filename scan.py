#!/usr/bin/env python
# coding: utf-8

import os

from scanner.libs.banner import print_banner
from scanner.libs.args import parse_cmd_options
from scanner.libs.request import patch_requests
from scanner.libs.plugins import get_plugins
from scanner.libs.targets import get_targets
from scanner.libs.threads import run_threads
from scanner.libs.scan.ports import Masscan
from scanner.libs.result import save_result


def _port_scan(args):
    """Port scan"""

    ms = Masscan(args)
    ms.scan()
    result = ms.parse_result_xml()

    return result


def _vuln_scan(args):
    """Vuln scan"""

    patch_requests(args)

    urls = args.url

    plugins = get_plugins(path=args.plugin_directory)

    if args.plugin:
        if os.path.dirname(args.plugin):
            plugins = get_plugins(path=os.path.dirname(args.plugin))
            plugins_name = [os.path.basename(args.plugin)]
        else:
            plugins_name = [args.plugin]
    else:
        plugins_name = plugins.list_plugins()

    targets = get_targets(args.pattern, urls, plugins=plugins_name)

    result = run_threads(targets, args, plugins=plugins)

    return result


def _sens_scan(args):
    """Sens scan"""

    patch_requests(args)

    urls = args.url

    targets = get_targets(args.pattern, urls, wordlist=args.wordlist)

    result = run_threads(targets, args)

    return result


def main():
    """Entry function"""

    print_banner()
    args = parse_cmd_options()
    
    if args.pattern == 'port':
        result = _port_scan(args)
    elif args.pattern == 'vuln':
        result = _vuln_scan(args)
    else:
        result = _sens_scan(args)
    
    save_result(args.pattern, result, args.output, args.db)


if __name__ == '__main__':
    main()
