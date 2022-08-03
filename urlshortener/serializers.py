from dynamic_db_router import in_database

from django.conf import settings

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from urlshortener.models import UrlShortener
from urlshortener.helpers import (
    create_random_url,
    check_if_random_url_already_generated,
    is_valid_url,
)


class UrlShortenerCreateSerializer(serializers.Serializer):
    shortened_url = serializers.CharField(required=False, allow_null=True)
    original_url = serializers.CharField(required=True, max_length=500)

    @in_database('default')
    def validate(self, attrs):
        original_url = attrs['original_url']
        if UrlShortener.objects.filter(original_url=original_url):
            msg = ('This url already shortened. You can check the list of '
                   'shortened urls')
            raise ValidationError(msg)

        if not is_valid_url(original_url):
            msg = 'Not a valid url. Make sure to copy full url'
            raise ValidationError(msg)
        return attrs

    def create(self, validated_data):
        shortened_url = create_random_url()
        while check_if_random_url_already_generated(shortened_url):
            shortened_url = create_random_url()
        validated_data.update(shortened_url=shortened_url)
        return UrlShortener.objects.create(**validated_data)


class UrlShortenerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlShortener
        fields = ['original_url', 'shortened_url', 'counter']


class UrlShortenerRedirectSerializer(serializers.Serializer):
    counter = serializers.IntegerField()
    original_url = serializers.CharField()
    shortened_url = serializers.CharField()

    def to_representation(self, instance):
        data = super(UrlShortenerRedirectSerializer, self).to_representation(
            instance)
        instance.counter += 1
        instance.save(update_fields=['counter'])

        return data
