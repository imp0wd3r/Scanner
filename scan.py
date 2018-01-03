#!/usr/bin/env python
# coding: utf-8

import os

from scanner.libs.banner import print_banner
from scanner.libs.args import parse_cmd_options
from scanner.libs.request import patch_requests
from scanner.libs.plugins import get_plugins
from scanner.libs.targets import get_targets
from scanner.libs.threads import run_threads
from scanner.libs.ports import Masscan
from scanner.libs.result import save_result
from scanner.utils import std_url


def _vuln_scan(args):
    """Vuln scan"""

    patch_requests(args)

    urls = []
    if args.url:
        urls.append(std_url(args.url))
    else:
        with open(args.url_file, 'r') as f:
            for url in f:
                urls.append(std_url(url.strip()))
        urls = list(set(urls))

    plugins = get_plugins(path=args.plugin_directory)

    if args.plugin:
        if os.path.dirname(args.plugin):
            plugins = get_plugins(path=os.path.dirname(args.plugin))
            targets = get_targets(urls, [os.path.basename(args.plugin)])
        else:
            targets = get_targets(urls, [args.plugin])
    else:
        targets = get_targets(urls, plugins.list_plugins())

    result = run_threads(targets, plugins, args)

    return result


def _port_scan(args):
    """Port scan"""

    ms = Masscan(args)
    ms.scan()
    result = ms.parse_result_xml()

    return result


def main():
    """Entry function"""

    print_banner()
    args = parse_cmd_options()
    
    if args.pattern == 'vuln':
        result = _vuln_scan(args)
    else:
        result = _port_scan(args)
    
    save_result(args.pattern, result, args.output, args.db)


if __name__ == '__main__':
    main()
