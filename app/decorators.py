from functools import wraps

def log_method(func):
    @wraps(func)
    def inner(*args, **kwargs):
        self = args[0]

        self.log.debug('>>> Executing {0}'.format(func.__name__), extra={'name_override': func.__name__})
        ret = func(*args, **kwargs)
        self.log.debug('<<< Finished {0}'.format(func.__name__), extra={'name_override': func.__name__})

        return ret

    return inner