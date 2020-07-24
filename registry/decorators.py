from absl import logging

from functools import wraps
import grpc

""" Decorator to check presence of a mandatory request argument and fail with an empty proto of provided type
"""
def must_have(kwarg, proto, nested=None):
    def must_have_decorator(func):
        @wraps(func)
        def func_wrapper(self, request, context):
            logging.debug('Checking must_have param {arg} for {service}'.format(arg=kwarg, service=func.__name__))
            logging.debug('Typeof request: {request}'.format(request=type(request)))
            if nested:
                nested_obj = getattr(request, nested)
                if getattr(nested_obj, kwarg):
                    return True
                else:
                    return False
            elif getattr(request, kwarg):
                return func(self, request, context)
            else:
                return fail_with_empty(
                        errormessage='Mandatory argument {arg} for {service} not provided'.format(arg=kwarg, service=func.__name__),
                        code=grpc.StatusCode.INVALID_ARGUMENT,
                        context=context,
                        proto=proto)
        return func_wrapper
    return must_have_decorator

def must_have_any(kwargs, proto):
    def must_have_any_decorator(func):
        @wraps(func)
        def func_wrapper(self, request, context):
            logging.debug('Checking must_have_any params {arg} for {service}'.format(arg=kwargs, service=func.__name__))
            logging.debug('Typeof request: {request}'.format(request=type(request)))
            found = False
            for kwarg in kwargs:
                if getattr(request, kwarg):
                    logging.debug('Found one: {kwarg}:{value}({typeof})'.format(kwarg=kwarg, value=getattr(request, kwarg), typeof=type(getattr(request, kwarg))))
                    found = True
                    break
            if found:
                return func(self, request, context)
            else:
                return fail_with_empty(
                        errormessage='One of the these arguments {arg} must be provided for {service}.'.format(arg=kwargs, service=func.__name__),
                        code=grpc.StatusCode.INVALID_ARGUMENT,
                        context=context,
                        proto=proto)
        return func_wrapper
    return must_have_any_decorator

def fail_with_empty(errormessage, code, context, proto):
    logging.error('Malformed grpc call from {client}: {error}'.format(client=context.peer(), error=errormessage))
    context.set_code(code)
    context.set_details(errormessage)
    return proto()
