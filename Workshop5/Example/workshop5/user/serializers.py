from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UpdatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']

    def update(self, instance,validated_data):
        
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        try:
            if validated_data['avatar']:
                instance.avatar = validated_data['avatar']
        except:
            pass
        instance.save()
        return instance