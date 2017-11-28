import sys
from multiprocessing.dummy import Pool

from scanner.libs.log import logger
from scanner.libs.exception import exception_handler


def run_threads(targets, plugins, args):
    """Create a thread pool and run the task."""

    thread_num = 5 if not args.threads else int(args.threads)
    p = Pool(thread_num)
    r_list = []
    result = []

    for target in targets:
        plugin = plugins.load_plugin(target['plugin'])
        r_list.append(p.apply_async(exception_handler, (plugin.poc, target['url'], args.extra_params)))

    p.close()

    try:
        for r in r_list:
            result.append(r.get())
        p.join()
    except KeyboardInterrupt:
        p.terminate()
        logger.failure('User aborted')
        sys.exit(1)

    return result
