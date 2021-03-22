from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
# from rest_framework.decorators import action


class UserView(ViewSet):
    def list(self, request):
        app_user = User.objects.get(pk=request.auth.user.id)
        serialized_user = UserSerializer(app_user, many=False, context={'request': request})
        return Response(serialized_user.data, status=status.HTTP_200_OK)
  

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for User"""
    full_name = serializers.CharField(source='get_full_name')
    class Meta:
        model = User
        fields= ('full_name', )
