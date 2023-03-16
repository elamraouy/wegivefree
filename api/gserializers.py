import hashlib
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from gifts.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "email", "first_name", "last_name")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        token = Token.objects.create(user=user)
        token.save()
        preferred_avatar_size_pixels = 256
        picture_url = "http://www.gravatar.com/avatar/{0}?s={1}".format(
            hashlib.md5(user.email.encode('UTF-8')).hexdigest(),
            preferred_avatar_size_pixels
        )
        profile = Profile(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            user_image=picture_url)
        if profile.save():
            return Response({"success": "true"})
        else:
            return Response({"success": "false"})


class GiftSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')
    formated_date = serializers.SerializerMethodField('get_format_date')

    class Meta:
        model = Mygifts
        fields = ['id',
                  'gived_by',
                  'title',
                  'body',
                  'domaine',
                  'city',
                  'user_image',
                  'user_name',
                  'image_url',
                  'formated_date',
                  'is_given'
                  ]

    @staticmethod
    def get_image_url(obj):
        if obj is not None:
            return obj.image.url

    @staticmethod
    def get_format_date(obj):
        if obj is not None:
            return obj.date_add.strftime('%d %b %Y %H:%M:%S')




