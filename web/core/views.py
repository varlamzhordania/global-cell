from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import translate_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import check_for_language


def set_language(request, *args, **kwargs):
    """
    Redirect to a given URL while setting the chosen language in the session
    (if enabled) and in a cookie. The URL and the language code need to be
    specified in the request parameters.

    This view changes how the user will see the rest of the site, so it must
    only be accessed via a GET request with query parameters.
    """
    next_url = request.GET.get("next")
    if (
            next_url or request.accepts("text/html")
    ) and not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = request.META.get("HTTP_REFERER")
        if not url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
        ):
            next_url = "/"

    lang_code = request.GET.get('language')
    if lang_code and check_for_language(lang_code):
        if next_url:
            next_trans = translate_url(next_url, lang_code)
            if next_trans != next_url:
                response = HttpResponseRedirect(next_trans)
            else:
                response = HttpResponseRedirect(next_url)
        else:
            response = HttpResponse(status=204)

        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
    else:
        response = HttpResponseRedirect(next_url) if next_url else HttpResponse(status=204)

    return response
