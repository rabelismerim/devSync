"""devsync URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import include, path, re_path

from .views import frontend_index


urlpatterns = [

    path('devsync/admin/', admin.site.urls),

    *([path('devsync/', include('core.identity.urls'))] if settings.IDENTITY_ENABLED else [
        path('devsync/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    ]),

    path('devsync/api/', include('main.record.urls')),

    re_path(r'^(?!devsync\/static|devsync\/documents|devsync\/login|devsync\/admin|devsync\/api).*$', frontend_index, name='frontend'),

    # just for DEBUG=True
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
