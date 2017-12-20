from threading import Thread


# This is a decorator that allows a function to run asynchronously in its own thread!
# It uses Python's thread library and starts the function in question inside a thread
def async(fn):
    def decorator(*args, **kwargs):
        t = Thread(target=fn, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator
