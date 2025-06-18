from cities_light.models import Region, City, Country, SubRegion
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserCreateSerializer(Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    user_type = serializers.IntegerField()

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    @staticmethod
    def validate_email(email):
        """
        Validate if email is already in use or not
        """
        email_already_active = User.objects.filter(email__iexact=email, is_active=True)
        if email_already_active:
            raise ValidationError(
                _("A user is already registered with this e-mail address."))
        else:
            users = User.objects.filter(email__iexact=email, is_active=False)
            for user in users:
                user.delete()
        return email

    def create(self, validated_data):
        email = validated_data['email']

        user = User(
            email=email,
            username=email,
            is_active=True,
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'name',
                  'email',
                  'is_active',
                  'username',
                  'description',
                  'birth_date',
                  ]


class UserLoginResponseSerializer(Serializer):
    class Meta:
        model = User

    def to_representation(self, instance):
        """
        Override the default to_representation method to format the data as needed
        """
        token = TokenObtainPairSerializer.get_token(instance)
        ret = {
            'access': str(token.access_token),
            'refresh': str(token),
            'user': UserDetailSerializer(instance).data,
        }
        return ret


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name',
            'description',
            'birth_date',
        ]


class CountrySerializer(ModelSerializer):
    """
    Serializer for the Country model
    """

    class Meta:
        model = Country
        fields = ['id', 'name']


class RegionSerializer(ModelSerializer):
    """
    Serializer for the Region/State model
    """

    class Meta:
        model = Region
        fields = ['id', 'name']


class SubRegionSerializer(ModelSerializer):
    """
    Serializer for the Region/State model
    """
    region = RegionSerializer()

    class Meta:
        model = SubRegion
        fields = ['id', 'name', 'region']


class CitySerializer(ModelSerializer):
    """
    Serializer for City model.
    """
    id = serializers.IntegerField(allow_null=True)
    country = CountrySerializer(read_only=True)
    subregion = SubRegionSerializer(read_only=True)
    region = RegionSerializer(read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'subregion', 'region', 'country']
