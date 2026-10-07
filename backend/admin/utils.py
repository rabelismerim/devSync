from django.conf import settings
from django.contrib.admin.utils import (
    NestedObjects, NoReverseMatch,
    router, capfirst, reverse, quote, format_html
)


def get_admin_overrides(model=None):
    model_data = None
    if (hasattr(settings, 'ADMIN_OVERRIDES') and isinstance(settings.ADMIN_OVERRIDES, dict)):
        if model is not None:
            for app_models in settings.ADMIN_OVERRIDES.values():
                model_data = next(
                    (
                        item
                        for item in app_models
                        if item[0] == model._meta.app_label
                            and item[1] == model._meta.object_name
                    ),
                    None
                )
                if model_data is not None:
                    break
        else:
            model_data = settings.ADMIN_OVERRIDES

    return (
        model_data
        or (
            model
            and (
                model._meta.app_label,
                model._meta.object_name,
                model._meta.verbose_name,
                model._meta.verbose_name_plural
            )
        )
    )


def get_deleted_objects(objs, request, admin_site):
    """
    Find all objects related to ``objs`` that should also be deleted. ``objs``
    must be a homogeneous iterable of objects (e.g. a QuerySet).

    Return a nested list of strings suitable for display in the
    template with the ``unordered_list`` filter.
    """
    try:
        obj = objs[0]
    except IndexError:
        return [], {}, set(), []
    else:
        using = router.db_for_write(obj._meta.model)
    collector = NestedObjects(using=using)
    collector.collect(objs)
    perms_needed = set()

    def format_callback(obj):
        model = obj.__class__
        has_admin = model in admin_site._registry
        opts = obj._meta
        opts_overrides = get_admin_overrides(obj)

        obj_str = hasattr(obj, 'full_labelled_name') and obj.full_labelled_name() or str(obj)

        no_edit_link = '%s: %s' % (capfirst(opts_overrides[2]), obj_str)

        if has_admin:
            if not admin_site._registry[model].has_delete_permission(request, obj):
                perms_needed.add(opts_overrides[2])
            try:
                admin_url = reverse('%s:%s_%s_change'
                                    % (admin_site.name,
                                       opts.app_label,
                                       opts.model_name),
                                    None, (quote(obj.pk),))
            except NoReverseMatch:
                # Change url doesn't exist -- don't display link to edit
                return no_edit_link

            # Display a link to the admin page.
            return format_html('{}: <a href="{}">{}</a>',
                               capfirst(opts_overrides[2]),
                               admin_url,
                               obj_str)
        else:
            # Don't display link to edit, because it either has no
            # admin or is edited inline.
            return no_edit_link

    to_delete = collector.nested(format_callback)

    protected = [format_callback(obj) for obj in collector.protected]
    model_count = {
        get_admin_overrides(model)[3]: len(objs)
        for model, objs in collector.model_objs.items()
    }

    return to_delete, model_count, perms_needed, protected
