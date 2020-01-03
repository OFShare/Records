from functools import wraps

def logit(logfile='out.log'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string,'\n','test3333....')  
        print('test2222....')
        return wrapped_function
    print('test1111....')
    return logging_decorator

# myfunc1=logit()(myfunc1)
@logit()
def myfunc1():
    pass

myfunc1()