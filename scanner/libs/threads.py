import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from scanner.libs.log import logger
from scanner.libs.exception import exception_handler
from scanner.libs.scan.sens import sens_scan


def _run_vuln_task(executor, targets, plugins, args):
    task_list = set()

    for target in targets:
        plugin = plugins.load_plugin(target['plugin'])
        task_list.add(
            executor.submit(
                exception_handler, 
                'vuln',
                plugin.poc, 
                target['url'], 
                args.extra_params
            )
        )
    
    return task_list


def _run_sens_task(executor, targets, args):
    task_list = set()

    for target in targets:
        task_list.add(
            executor.submit(
                exception_handler, 
                'sens',
                sens_scan, 
                target, 
                args.timeout
            )
        )
    
    return task_list


def run_threads(targets, args, plugins=None):
    """Create a thread pool and run the task"""

    thread_num = int(args.threads)
    result = []

    with ThreadPoolExecutor(max_workers=thread_num) as executor:
        if args.pattern == 'vuln':
            task_list = _run_vuln_task(executor, targets, plugins, args)
        else:
            task_list = _run_sens_task(executor, targets, args)

        try:
            for future in as_completed(task_list):
                if future.result():
                    result.append(future.result())
        except KeyboardInterrupt:
            logger.failure('User aborted')
            os._exit(1)

    return result
