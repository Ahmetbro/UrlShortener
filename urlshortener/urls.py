from rest_framework import routers
from django.conf.urls import url, include

from urlshortener.views import UrlShortenerViewset

router = routers.SimpleRouter()
router.register(r'',
                UrlShortenerViewset,
                base_name='url-shortener')

urlpatterns = router.urls
