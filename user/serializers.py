from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.serializers import \
    AuthTokenSerializer as BaseAuthTokenSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user objects.
    """

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {
                'min_length': 4,
                'write_only': True,
            }
        }

    def create(self, validated_data):
        """
        Override to create objects in need of validation.
        :param validated_data:
        :return: user
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        update a user with validated_data,
        setting password correctly into database.
        :return: user
        """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,  # By default, django will trim off whitespace in password.
    )

    def validate(self, attrs):
        """
        Validate and authenticate the user.
        Check if the inputs are correct.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),  # get from serializer->context
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            # serializer will handle this error by Response HTTP400
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        # Whenever validate attributes, must return attributes back.
        return attrs
