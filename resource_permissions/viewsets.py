from .decorators import permission_wrapper

class PermissionViewSetMixin:

    def __init__(self, **kwargs):
        view_methods = (
            'list',
            'retrieve',
            'create',
            'update',
            'partial_update',
            'destroy'
        )

        for action in view_methods:
            method = getattr(self, action, None)
            if method:
                setattr(self, method.__name__, permission_wrapper(method))