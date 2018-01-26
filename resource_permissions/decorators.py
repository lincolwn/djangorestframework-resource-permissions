import warnings

def check_permissions(*args, **kwargs):
    view = args[0]
    request = args[1]
    view.check_action_permissions(request, func.__name__)


def permission_wrapper(*args, **kwargs):
    '''
    must be used to wraps default viewset methods view
    '''
    def decorator(func):
        check_permissions(*args, **kwargs)
        return func(*args, **kwargs)
    return decorator


def action(methods=None, detail=None, url_path=None, url_name=None, *args, **kwargs):
    '''
    Same of 'action' decorator from django rest framework, with a litle 
    customization:

    Add permision verification before body method execution
    '''
    methods = ['get'] if (methods is None) else methods
    methods = [method.lower() for method in methods]

    assert detail is not None, (
        "@action() missing required argument: 'detail'"
    )

    def decorator(func):
        func.bind_to_methods = methods
        func.detail = detail
        func.url_path = url_path or func.__name__
        func.url_name = url_name or func.__name__.replace('_', '-')
        func.kwargs = kwargs
        return func(*args, **kwargs)
    return decorator


def detail_route(methods=None, *args, **kwargs):
    '''
    Same of 'detail_route' of drf with '*args' parameter
    '''
    warnings.warn(
        "`detail_route` is pending deprecation and will be removed in 3.10 in favor of "
        "`action`, which accepts a `detail` bool. Use `@action(detail=True)` instead.",
        PendingDeprecationWarning, stacklevel=2
    )
    return action(methods, detail=True, *args, **kwargs)


def list_route(methods=None, **kwargs):
    """
    Same of 'list_route' of drf with '*args' parameter
    """
    warnings.warn(
        "`list_route` is pending deprecation and will be removed in 3.10 in favor of "
        "`action`, which accepts a `detail` bool. Use `@action(detail=False)` instead.",
        PendingDeprecationWarning, stacklevel=2
    )
    return action(methods, detail=False, **kwargs)