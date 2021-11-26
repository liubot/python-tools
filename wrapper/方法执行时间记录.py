import time
import functools
from log import log
logger = log.init()
'''
    用于记录方法的执行时间
    输出方法的执行文件、方法名称、耗时
    可以配合logging日志模块使用，也可以使用print代替。
'''
def cost_time(func):
    @functools.wraps(func)
    def inner(*args,**kwargs):
        start_time = time.time()
        res = func(*args,**kwargs)
        end_time = time.time()
        cost = end_time - start_time
        logger.debug("{} -> {} costTime:{} s".format(func.__code__.co_filename,func.__name__,cost))
        return res
    return inner

@cost_time
def foo():
    time.sleep(1.2)

@cost_time
def f1():
    foo()
    time.sleep(1)

if __name__ == "__main__":
    f1()
    '''
    result
    [2021-11-26 18:27:01,597 - 方法执行时间记录.py - DEBUG] D:/gitspace/python-tools/wrapper/方法执行时间记录.py -> foo costTime:1.2000782489776611 s
    [2021-11-26 18:27:02,597 - 方法执行时间记录.py - DEBUG] D:/gitspace/python-tools/wrapper/方法执行时间记录.py -> f1 costTime:2.2005937099456787 s
    '''
