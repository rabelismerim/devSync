from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.encoding import iri_to_uri

# from rest_framework.status import HTTP_200_OK
# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.authentication import SessionAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response


ms_identity_web = settings.IDENTITY_IDENTITY_WEB

@require_GET
@never_cache
def login(request):
    if request.user.is_authenticated:
        # Already logged-in, redirect to index
        return redirect('/devsync/')

    if ms_identity_web is None:
        return redirect('/devsync/admin/login/?next=/devsync/')
    next_url = request.GET.get('next', '/devsync/')
    if not url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
        next_url = '/devsync/'
    auth_url = ms_identity_web.get_auth_url(
        redirect_uri=request.build_absolute_uri(
            reverse('login_msal_redirect', kwargs={'redirect_uri': next_url})
        )
    )
    return redirect(auth_url)

@require_GET
@never_cache
def login_msal_redirect(request, redirect_uri):
    if url_has_allowed_host_and_scheme(redirect_uri, {request.get_host()}):
        ms_identity_web.process_auth_redirect(
            request,
            redirect_uri=request.build_absolute_uri(request.path),
        )
        return redirect(iri_to_uri(redirect_uri))
    return HttpResponseBadRequest('Destino inválido.')

# @api_view(['GET'])
# @authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
# def get_user_picture(request):
#     return Response(data={

#     }, status=HTTP_200_OK)
