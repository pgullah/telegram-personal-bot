from __future__ import print_function
import sys
import threading
try:
    import thread # pyright: ignore [reportMissingImports]
except ImportError:
    import _thread as thread

AMDIN_IDS = ['50770706']

def AdminOnly(func):
    def wrapper(*args, **kwargs):
        chat_id = args[0].effective_chat.id
        if str(chat_id) in AMDIN_IDS:
           return func(*args, **kwargs)
        else:
           print("{} is not entitled to access the resource: '{}' ".format(chat_id, func.__name__))
           return None

    return wrapper

def __quit_function(fn_name):
    # print to stderr, unbuffered in Python 2.
    print('{0} took too long'.format(fn_name), file=sys.stderr)
    sys.stderr.flush() # Python 3 stderr is likely buffered.
    thread.interrupt_main() # raises KeyboardInterrupt

def exit_after(sec):
    '''
    use as decorator to exit process if 
    function takes longer than x seconds
    '''
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(sec, __quit_function, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer