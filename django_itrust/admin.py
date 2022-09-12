from django.apps import apps
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


class ITrustUserAdmin(DefaultUserAdmin):
    if apps.is_installed("django_su"):  # pragma: no cover
        change_form_template = "admin/auth/user/change_form.html"
        change_list_template = "admin/auth/user/change_list.html"
