from django.conf import settings
from components import AllowAny
from django.test.signals import setting_changed

def update_setting(*args, **kwargs):
    setting = kwargs['setting']
    if setting == 'DSR_RESOURCE_PERMISSIONS_CLASSES':
        try:
            perms_settings.DSR_RESOURCE_PERMISSIONS_CLASSES = kwargs['value']
        except KeyError:
            pass


class PermissionSettings:
    
    def __init__(self):
        self.DSR_RESOURCE_PERMISSIONS_CLASSES = \
            getattr(settings, 'DSR_RESOURCE_PERMISSIONS_CLASSES', (AllowAny,))

    
perms_settings = PermissionSettings()

setting_changed.connect(update_setting)