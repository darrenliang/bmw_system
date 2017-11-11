from rest_framework import serializers
from django.contrib.auth.models import User


class UserWithoutUsernameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',)
        
    '''
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password', 'snippets',)
        
        extra_kwargs = {
            'password': {'write_only': True},
        }
    '''  
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)



