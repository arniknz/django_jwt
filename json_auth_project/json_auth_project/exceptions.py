import rest_framework.views


def core_exception_handler(exc, context):
    respone = rest_framework.views.exception_handler(exc=exc, context=context)
    handlers = {
        'ValidationError': _handle_generic_error,
    }

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, respone)

    return respone


def _handle_generic_error(exc, context, response):
    response.data = {
        'errors': response.data
    }

    return response
