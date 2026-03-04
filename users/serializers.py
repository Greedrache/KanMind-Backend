from rest_framework import serializers
from users.models import UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']


class RegistrationSerializer(serializers.Serializer):
    fullname = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    repeated_password = serializers.CharField(write_only=True, required=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def validate(self, data):
        if data.get('password') != data.get('repeated_password'):
            raise serializers.ValidationError({"repeated_password": "Passwords do not match."})
        return data

    def save(self):
        fullname = self.validated_data['fullname']
        email = self.validated_data['email']
        password = self.validated_data['password']

        user = User(
            username=email,
            email=email,
            first_name=fullname
        )
        user.set_password(password)
        user.save()
        return user