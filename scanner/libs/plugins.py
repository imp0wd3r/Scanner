import os
import sys

from scanner.libs.pluginbase import PluginBase
from scanner.libs.log import logger


def get_plugins(path='./plugins'):
    """Get plugins object via PluginBase."""

    if os.path.exists(path):
        plugin_base = PluginBase(package='scan_plugins')
        plugin_source = plugin_base.make_plugin_source(searchpath=[path])
        return plugin_source
    else:
        logger.failure('The plugin directory was not found (default: ./plugins).')
        sys.exit(1)
