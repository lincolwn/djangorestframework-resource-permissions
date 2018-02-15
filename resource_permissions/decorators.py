import warnings

# def check_permissions(*args, **kwargs):
#     view = func.__self__
#     view.check_action_permissions(request, func.__name__)


def permission_wrapper(func):
    '''
    must be used to wraps default viewset methods view
    '''
    def wrapper(*args, **kwargs):
        view = func.__self__
        request = args[0]
        view.check_action_permissions(request, func.__name__)
        return func(*args, **kwargs)
    return wrapper


def action(methods=None, detail=None, url_path=None, url_name=None, **kwargs):
    """
    Mark a ViewSet method as a routable action.
    Set the `detail` boolean to determine if this action should apply to
    instance/detail requests or collection/list requests.
    """
    methods = ['get'] if (methods is None) else methods
    methods = [method.lower() for method in methods]

    assert detail is not None, (
        "@action() missing required argument: 'detail'"
    )

    def decorator(func):
        def wrapper(*args, **kwargs):
            view = args[0]
            request = args[1]
            view.check_action_permissions(request, func.__name__)
            return func(*args, **kwargs)
        wrapper.bind_to_methods = methods
        wrapper.detail = detail
        wrapper.url_path = url_path or func.__name__
        wrapper.url_name = url_name or func.__name__.replace('_', '-')
        wrapper.kwargs = kwargs
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator


def detail_route(methods=None, **kwargs):
    """
    Used to mark a method on a ViewSet that should be routed for detail requests.
    """
    warnings.warn(
        "`detail_route` is pending deprecation and will be removed in 3.10 in favor of "
        "`action`, which accepts a `detail` bool. Use `@action(detail=True)` instead.",
        PendingDeprecationWarning, stacklevel=2
    )
    return action(methods, detail=True, **kwargs)


def list_route(methods=None, **kwargs):
    """
    Used to mark a method on a ViewSet that should be routed for list requests.
    """
    warnings.warn(
        "`list_route` is pending deprecation and will be removed in 3.10 in favor of "
        "`action`, which accepts a `detail` bool. Use `@action(detail=False)` instead.",
        PendingDeprecationWarning, stacklevel=2
    )
    return action(methods, detail=False, **kwargs)


def get_object_wrapper(func):
    '''
    Change 'get_object' implementation for 'wrapper'. 'wrapper' function
    is same of 'get_object' from django rest framework with some customizations
    referent to permission verification.
    '''
    def wrapper(*args):
        from rest_framework.generics import get_object_or_404
        self = func.__self__

        action = getattr(self, self.request.method.lower())
        action = action.__name__
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, action, obj)
        return obj
    wrapper.__name__ = func.__name__
    return wrapper