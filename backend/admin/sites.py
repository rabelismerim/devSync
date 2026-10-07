# from functools import update_wrapper

from django.contrib import admin
# from django.shortcuts import redirect
# from django.views.decorators.cache import never_cache
# from django.views.decorators.csrf import csrf_protect
# from django.urls import reverse

from .utils import get_admin_overrides, get_deleted_objects

# methods/functions/properties to override admin.ModelAdmin class
def prop_getter_model(self):
    return self._model

def prop_setter_model(self, value):
    if hasattr(value, '_meta'):
        model_overrides = get_admin_overrides(value)
        value._meta.verbose_name = model_overrides[2].lower()
        value._meta.verbose_name_plural = model_overrides[3].lower()
    self._model = value


def get_deleted_objects_override(self, objs, request):
    return get_deleted_objects(objs, request, self.admin_site)
#\ methods/functions to override on admin.ModelAdmin class


class DevSyncAdminSite(admin.AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = 'DevSync'

    # Text to put in each page's <h1>.
    site_header = 'DevSync'

    # Text to put at the top of the admin index page.
    index_title = ''

    # URL for the "View site" link at the top of each admin page.
    site_url = ''

    enable_nav_sidebar = False


    def register(self, model_or_iterable, admin_class=None, **options):
        admin_class = admin_class or admin.ModelAdmin
        setattr(admin_class, 'model', property(prop_getter_model, prop_setter_model))
        setattr(admin_class, 'get_deleted_objects', get_deleted_objects_override)
        super().register(model_or_iterable, admin_class, **options)


    # def admin_view(self, view, cacheable=False):
    #     def inner(request, *args, **kwargs):
    #         if not self.has_permission(request):
    #             if request.user.is_authenticated:
    #                 return redirect('/?admin=401')
    #             return redirect(
    #                 reverse('identity_signin', kwargs={'redirect_uri': ''})
    #             )
    #         return view(request, *args, **kwargs)
    #     if not cacheable:
    #         inner = never_cache(inner)
    #     if not getattr(view, 'csrf_exempt', False):
    #         inner = csrf_protect(inner)
    #     return update_wrapper(inner, view)


    # def get_urls(self):
    #     urlpatterns = [
    #         urlpattern
    #         for urlpattern in super().get_urls()
    #         if getattr(urlpattern, 'name', None) not in [
    #             'login', 'logout', 'password_change', 'password_change_done'
    #         ]
    #     ]
    #     return urlpatterns


    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        admin_overrides = get_admin_overrides()
        if admin_overrides:
            models_list = [
                {
                    'app_label': app_data['app_label'],
                    **model_data
                }
                for app_data in app_list
                for model_data in app_data['models']
            ]

            app_list = []
            for app_name, app_models in admin_overrides.items():
                models_data = []
                for m_app_label, m_object_name, _1, m_verbose_name_plural, m_visible in app_models:
                    if not m_visible:
                        continue
                    model_data = next(
                        (
                            item
                            for item in models_list
                            if item['app_label'] == m_app_label
                                and item['object_name'] == m_object_name
                        ),
                        None
                    )
                    if model_data is not None:
                        model_data['name'] = m_verbose_name_plural
                        models_data.append(model_data)

                if models_data:
                    app_list.append({
                        'name': app_name,
                        'app_label': None,
                        'app_url': None,
                        'has_module_perms': True,
                        'models': models_data
                    })

        return app_list
