def get_targets(urls, plugins):
    """Use URLs and plugins' name to get the targets"""

    targets = []

    for url in urls:
        for plugin in plugins:
            targets.append({'url': url, 'plugin': plugin})

    return targets
