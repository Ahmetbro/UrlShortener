from urllib.parse import urlparse
import random
import string

from django.conf import settings

from urlshortener.models import UrlShortener


def create_random_url():
    length = random.randint(10, 20)
    allowed_characters = string.ascii_letters + string.digits
    url = ''.join(random.choice(allowed_characters) for i in range(length))
    return url


def check_if_random_url_already_generated(shortened_url):
    url = UrlShortener.objects.filter(shortened_url=shortened_url)
    if url:
        return True
    return False


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def prepare_result(data):
    prefix = settings.API_URL
    url = data['shortened_url']
    return {'result': prefix+url}
