from rest_framework import serializers

from user.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=100)
    password2 = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password1')
        if password == validated_data.pop('password2'):
            user = super().create(validated_data)
            user.set_password(password)
            user.save()
            return user
        self.error_messages.update({'error': "passwords doesn't match"})
