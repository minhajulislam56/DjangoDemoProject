from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(style={'input_type': 'Password'}, write_only=True)    # Disable it for showing password hash in shell
    password2 = serializers.CharField(style={'input_type': 'Password'}, write_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2'
        ]
        extra_kwargs = {
            'password': {'write_only': True},     # Disable it for showing password hash in shell
        }

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("email already exists")
        return value

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("username already exists")
        return value

    def validate(self, data):
        pw = data.get('password')
        pw2 = data.get('password2')
        if pw != pw2:
            raise serializers.ValidationError("Passwords must be unique.")
        return data

    def create(self, validated_data):   # This one used for avoiding data errors which exists in the request data but not in the DB. Ex: Password2
        # print(validated_data)         #Forced Method
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')
        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj