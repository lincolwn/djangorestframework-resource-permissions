from rest_framework.serializers import HyperlinkedModelSerializer
from tests.app.models import Office, Issue
from django.contrib.auth.models import User

class OfficeSerializer(HyperlinkedModelSerializer):
    
    class Meta:
        model = Office
        fields = '__all__'


class IssueSerializer(HyperlinkedModelSerializer):
    
    class Meta:
        model = Issue
        fields = '__all__'


class UserSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')