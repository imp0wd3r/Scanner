import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from scanner.libs.log import logger
from scanner.libs.exception import exception_handler


def run_threads(targets, plugins, args):
    """Create a thread pool and run the task."""

    thread_num = 5 if not args.threads else int(args.threads)
    result = []

    with ThreadPoolExecutor(max_workers=thread_num) as executor:
        task_list = set()

        for target in targets:
            plugin = plugins.load_plugin(target['plugin'])
            task_list.add(executor.submit(exception_handler, plugin.poc, target['url'], args.extra_params))

        try:
            for future in as_completed(task_list):
                result.append(future.result())
        except KeyboardInterrupt:
            logger.failure('User aborted')
            os._exit(1)

    return result
