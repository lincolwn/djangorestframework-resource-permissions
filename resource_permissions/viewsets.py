from .decorators import permission_wrapper

class PermissionViewSetMixin:

    def __init__(self, **kwargs):
        super(PermissionViewSetMixin, self).__init__(**kwargs)
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


    def check_action_permissions(self, request, action):
        """
        Check if the request should be permitted to method that represents action.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.check_action_permissions(request, action):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )


    def check_object_permissions(self, request, action, obj):
        """
        Check if the request should be permitted to do action for given object.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.check_object_permissions(request, action, obj):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )
