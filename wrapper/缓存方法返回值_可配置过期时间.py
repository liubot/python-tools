from inspect import signature
import hashlib
from collections import namedtuple
import time
import functools
'''
author：liubo
函数装饰器缓存功能，支持过期时间：
    用于：  装饰带有返回值的函数，缓存函数返回结果，加快其响应时间。
    原理：  根据调用某个函数的基本信息和参数为唯一值判断，如果同一个函数并且相同参数，则返回缓存信息。
            第一次调用会将函数的基础信息（路径，首行行号，函数名，函数签名）的md5值作为外层key，内层key为函数参数的md5值，字典值为函数的返回值。
            第二次及以后调用会现根据方法id和参数id寻找是否存在缓存。如果存在，返回缓存的函数数据；否则，调用方法缓存其结果。
    可选参数：expire_second：必须为int,单位为秒。若果定义，将在定义时间内过期。如 expire_second=60 ：则60秒后此缓存过期。不填，则永不过期
'''

FunCache = namedtuple('FunCache',['file_path','first_lineno','func_name','sig','args','kwargs','res','expire_time'])

def md5_encode(_str):
    m = hashlib.md5()
    m.update(_str.encode(encoding='utf-8'))
    res = m.hexdigest()
    return res


def fun_cache(func=None,*,expire_second=None):
    if func is None:
        return functools.partial(fun_cache,expire_second=expire_second)
    cache_dict = {} #缓存数据
    #方法基础信息，判断唯一性
    file_path = func.__code__.co_filename
    first_lineno = func.__code__.co_firstlineno
    func_name = func.__name__
    sig = signature(func)
    func_id = md5_encode("{}|{}|{}|{}".format(file_path,first_lineno,func_name,sig))    #方法唯一id
    @functools.wraps(func)
    def inner(*args,**kwargs):
        #设置过期时间 = 当前时间 + 用户设置秒数
        expire_time = None
        if expire_second:
            if isinstance(expire_second, int):
                expire_time = int(time.time()) + expire_second
            else:
                raise ValueError("expire_second expected type Int!")

        args_id = md5_encode("{}{}".format(args, kwargs))   #参数唯一id
        res = None  #返回结果
        cache_func = cache_dict.get(func_id)
        if cache_func and cache_func.get(args_id):      #是否命中方法缓存和参数缓存
            # 返回缓存的2中情况：1、没有设置过期时间  2、过期时间大于当前时间
            if not cache_func.get(args_id).expire_time:
                res = cache_func.get(args_id).res
            if cache_func.get(args_id).expire_time and cache_func.get(args_id).expire_time > time.time():
                res = cache_func.get(args_id).res
        if not res:     #没有命中缓存
            cache_dict.setdefault(func_id,{})
            res = func(*args,**kwargs)
            if res:
                func_cache = FunCache(file_path,first_lineno,func_name,sig,args,kwargs,res,expire_time)
                cache_dict[func_id][args_id] = func_cache
        return res

    return inner



if __name__ == "__main__":
    #不带过期时间，生命周期内永久有效
    @fun_cache
    def bar(num):
        print("run in  bar:{}".format(num))
        return num**num

    #设置过期时间，2秒后过期
    @fun_cache(expire_second=2)
    def foo(num):
        print("run in  foo:{}".format(num))
        return num*2

    print (1,bar(2))  #第一次，不会使用缓存
    print (2,bar(2))  #第二次，使用缓存
    print (3,bar(5))  #参数不同，不会使用缓存
    print(4,foo(5))   #函数不同不会使用缓存，不会使用缓存
    print(5,foo(5))   #第二次，使用缓存,过期时间2秒
    time.sleep(3)
    print(6,foo(5))  #时间已过，不适用缓存
    print(7,bar(2))  #调用第一个方法，相同参数，使用缓存



