import concurrent.futures, queue, logging
from . import config

# futures not finshied
_futures = queue.Queue()

# thread pool executor object
_executor = concurrent.futures.ThreadPoolExecutor(max_workers=config.EXECUTOR_WORKERS, thread_name_prefix='atm')


def submit(fn, *args, **kwargs):
    """
        schedule a executable function fn
    :param fn:
    :param args:
    :param kwargs:
    :return:
    """
    future = _executor.submit(fn, *args, **kwargs)
    _futures.put(future)


def _takecare():
    """
        take care of future obejcts
    :return:
    """
    future = _futures.get()
    concurrent.futures.as_completed(future)

    try:
        logging.info('executed: %s' % future.result())
    except Exception as e:
        logging.error('executed: %s' % str(e))

    # take care next
    _executor.submit(_takecare)

# add take care task to thread pool executor
_executor.submit(_takecare)
