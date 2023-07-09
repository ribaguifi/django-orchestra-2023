from django.urls import re_path as url
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from orchestra.admin import ExtendedModelAdmin, ChangePasswordAdminMixin
from orchestra.admin.utils import change_url
from orchestra.contrib.accounts.actions import list_accounts
from orchestra.contrib.accounts.admin import SelectAccountAdminMixin

from .filters import HasUserListFilter, HasDatabaseListFilter
from .forms import DatabaseCreationForm, DatabaseUserChangeForm, DatabaseUserCreationForm, DatabaseForm
from .models import Database, DatabaseUser

def save_selected(modeladmin, request, queryset):
    for selected in queryset:
         selected.save()
save_selected.short_description = "Re-save selected objects"

class DatabaseAdmin(SelectAccountAdminMixin, ExtendedModelAdmin):
    list_display = ('name', 'type', 'display_users', 'account_link')
    list_filter = ('type', HasUserListFilter)
    search_fields = ('name', 'account__username')
    change_readonly_fields = ('name', 'type', 'target_server')
    extra = 1
    fieldsets = (
        (None, {
            'classes': ('extrapretty',),
            'fields': ('account_link', 'name', 'type', 'users', 'display_users', 'comments', 'target_server'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('account_link', 'name', 'type', 'target_server')
        }),
        (_("Create new user"), {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        (_("Use existing user"), {
            'classes': ('wide',),
            'fields': ('user',)
        }),
    )
    form = DatabaseForm
    add_form = DatabaseCreationForm
    readonly_fields = ('account_link', 'display_users',)
    filter_horizontal = ['users']
    # filter_by_account_fields = ('users',)
    # list_prefetch_related = ('users',)
    actions = (list_accounts, save_selected)

    @mark_safe
    def display_users(self, db):
        links = []
        for user in db.users.all():
            link = format_html('<a href="{}">{}</a>', change_url(user), user.username)
            links.append(link)
        return '<br>'.join(links)
    display_users.short_description = _("Users")
    display_users.admin_order_field = 'users__username'

    def save_model(self, request, obj, form, change):
        super(DatabaseAdmin, self).save_model(request, obj, form, change)
        if not change:
            user = form.cleaned_data['user']
            if not user:
                user = DatabaseUser(
                    username=form.cleaned_data['username'],
                    type=obj.type,
                    account_id=obj.account.pk,
                    target_server=form.cleaned_data['target_server'],
                )
                user.set_password(form.cleaned_data["password1"])
            user.save()
            obj.users.add(user)


class DatabaseUserAdmin(SelectAccountAdminMixin, ChangePasswordAdminMixin, ExtendedModelAdmin):
    list_display = ('username', 'target_server', 'type', 'display_databases', 'account_link')
    list_filter = ('type', HasDatabaseListFilter)
    search_fields = ('username', 'account__username')
    form = DatabaseUserChangeForm
    add_form = DatabaseUserCreationForm
    change_readonly_fields = ('username', 'type', 'target_server')
    fieldsets = (
        (None, {
            'classes': ('extrapretty',),
            'fields': ('account_link', 'username', 'password', 'type', 'display_databases', 'target_server', 'permision')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('extrapretty',),
            'fields': ('account_link', 'username', 'password1', 'password2', 'type', 'target_server', 'permision')
        }),
    )
    readonly_fields = ('account_link', 'display_databases',)
    filter_by_account_fields = ('databases',)
    list_prefetch_related = ('databases',)
    actions = (list_accounts, save_selected)

    @mark_safe
    def display_databases(self, user):
        links = []
        for db in user.databases.all():
            link = format_html('<a href="{}">{}</a>', change_url(db), db.name)
            links.append(link)
        return '<br>'.join(links)
    display_databases.short_description = _("Databases")
    display_databases.admin_order_field = 'databases__name'

    def get_urls(self):
        useradmin = UserAdmin(DatabaseUser, self.admin_site)
        return [
            url(r'^(\d+)/password/$',
                self.admin_site.admin_view(useradmin.user_change_password))
        ] + super(DatabaseUserAdmin, self).get_urls()

    def save_model(self, request, obj, form, change):
        """ set password """
        if not change:
            obj.set_password(form.cleaned_data["password1"])
        super(DatabaseUserAdmin, self).save_model(request, obj, form, change)


admin.site.register(Database, DatabaseAdmin)
admin.site.register(DatabaseUser, DatabaseUserAdmin)
