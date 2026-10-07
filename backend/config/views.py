from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def frontend_index(request):
    profile = None
    if request.user.is_authenticated:
        from main.record.serializers import UserFullSerializer
        profile = UserFullSerializer(request.user, context={'request': request}).data
    return render(request, 'frontend/index.html', {'usr_prf': profile})
