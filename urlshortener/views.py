from django.http import Http404
from django.shortcuts import redirect
from django.conf import settings

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import list_route

from urlshortener.helpers import prepare_result
from urlshortener.models import UrlShortener
from urlshortener.serializers import (
    UrlShortenerCreateSerializer,
    UrlShortenerListSerializer,
    UrlShortenerRedirectSerializer,
)


class UrlShortenerViewset(ModelViewSet):
    retrieve_serializer = UrlShortenerRedirectSerializer
    create_short_url_serializer = UrlShortenerCreateSerializer
    list_all_shortened_urls_serializer = UrlShortenerListSerializer
    lookup_field = "shortened_url"
    model = UrlShortener

    def get_serializer_class(self):
        if self.action == settings.ACTION_RETRIEVE:
            if hasattr(self, 'retrieve_serializer'):
                return self.retrieve_serializer
        elif self.action == settings.ACTION_CREATE_URL:
            if hasattr(self, 'create_short_url_serializer'):
                return self.create_short_url_serializer
        elif self.action == settings.ACTION_LIST_URLS:
            if hasattr(self, 'list_all_shortened_urls_serializer'):
                return self.list_all_shortened_urls_serializer
        return super(UrlShortenerViewset, self).get_serializer_class()

    def get_object(self, shortened_url):
        try:
            return UrlShortener.objects.get(shortened_url=shortened_url)
        except UrlShortener.DoesNotExist:
            raise Http404

    def get_queryset(self):
        return UrlShortener.objects.all()

    def retrieve(self, request, *args, **kwargs):
        #import ipdb; ipdb.set_trace()
        instance = self.get_object(kwargs.get('shortened_url'))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance)

        return redirect(
            serializer.data['original_url'],
            status=status.HTTP_301_MOVED_PERMANENTLY
        )

    @list_route(methods=['post'], url_path='create-url')
    def create_short_url(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        result = prepare_result(serializer.data)
        return Response(result, status=status.HTTP_201_CREATED)

    @list_route(methods=['get'], url_path='list-all-urls')
    def list_all_shortened_urls(self, request):
        queryset = self.get_queryset()
        serializer = UrlShortenerListSerializer(queryset, many=True)
        result = serializer.data
        return Response(result)
