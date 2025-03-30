import logging
from django.core.cache import cache
from django.conf import settings
import requests

logger = logging.getLogger(__name__)


class GeolocationMiddleware:
    CACHE_KEY_PREFIX = 'geolocation_'
    CACHE_TIMEOUT = 604800  # 1 week in seconds

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if a language is explicitly set in the URL
        language_from_url = self.get_language_from_url(request)
        if language_from_url:
            request.session['django_language'] = language_from_url
        else:
            user_ip = self.get_client_ip(request)
            user_location = self.get_user_location(user_ip)

            # Determine language based on location
            language_for_location = self.get_language_for_location(user_location)
            request.session['django_language'] = language_for_location

        response = self.get_response(request)
        return response

    def get_user_location(self, ip_address):
        cache_key = f"{self.CACHE_KEY_PREFIX}{ip_address}"
        ip_info = cache.get(cache_key)

        if ip_info:
            country = ip_info.get("country")
        else:
            try:
                url = f'http://ipinfo.io/{ip_address}?token={settings.IP_INFO_TOKEN}'
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
                data = response.json()
                country = data.get('country')
                cache.set(cache_key, data, self.CACHE_TIMEOUT)
            except requests.RequestException as e:
                logger.error(f"API request failed for IP {ip_address}: {str(e)}")
                country = None

        return country

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_language_for_location(self, location):

        language_groups = {
            'en': ['US', 'CA', 'GB', 'AU'],  # United States, Canada, United Kingdom, Australia
            'fr': ['FR', 'CA', 'BE', 'CH'],  # France, Canada, Belgium, Switzerland
            'es': ['ES', 'MX', 'AR', 'CO', 'PE'],  # Spain, Mexico, Argentina, Colombia, Peru
            'ar': ['JO', 'EG', 'SA', 'AE', 'KW'],  # Jordan, Egypt, Saudi Arabia, UAE, Kuwait
            # Add more language groups as needed
        }

        for language, countries in language_groups.items():
            if location in countries:
                return language

        return 'en'  # Default to English if no matching language group is found

    def get_language_from_url(self, request):
        # Extract language from the URL, if present
        language_from_url = request.path_info.split('/')[1]
        if language_from_url in dict(settings.LANGUAGES).keys():
            return language_from_url
        return None