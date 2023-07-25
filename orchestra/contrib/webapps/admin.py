from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.utils.translation import gettext, gettext_lazy as _

from orchestra.admin import ExtendedModelAdmin
from orchestra.admin.utils import admin_link, get_modeladmin
from orchestra.contrib.accounts.actions import list_accounts
from orchestra.contrib.accounts.admin import AccountAdminMixin
from orchestra.forms.widgets import DynamicHelpTextSelect
from orchestra.plugins.admin import SelectPluginAdminMixin, display_plugin_field
from orchestra.utils.html import get_on_site_link

from .filters import HasWebsiteListFilter, DetailListFilter
from .models import WebApp, WebAppOption
from .options import AppOption
from .types import AppType


class WebAppOptionInline(admin.TabularInline):
    model = WebAppOption
    extra = 1

    OPTIONS_HELP_TEXT = {
        op.name: force_str(op.help_text) for op in AppOption.get_plugins()
    }

    class Media:
        css = {
            'all': ('orchestra/css/hide-inline-id.css',)
        }

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'value':
            kwargs['widget'] = forms.TextInput(attrs={'size':'100'})
        if db_field.name == 'name':
            if self.parent_object:
                plugin = self.parent_object.type_class
            else:
                request = kwargs['request']
                webapp_modeladmin = get_modeladmin(self.parent_model)
                plugin_value = webapp_modeladmin.get_plugin_value(request)
                plugin = AppType.get(plugin_value)
            kwargs['choices'] = plugin.get_group_options_choices()
            # Help text based on select widget
            target = 'this.id.replace("name", "value")'
            kwargs['widget'] = DynamicHelpTextSelect(target, self.OPTIONS_HELP_TEXT)
        return super(WebAppOptionInline, self).formfield_for_dbfield(db_field, **kwargs)


class WebAppAdmin(SelectPluginAdminMixin, AccountAdminMixin, ExtendedModelAdmin):
    list_display = (
        'name', 'display_type', 'display_detail', 'display_websites', 'account_link'
    )
    list_filter = ('type', HasWebsiteListFilter, DetailListFilter)
    inlines = [WebAppOptionInline]
    readonly_fields = ('account_link',)
    change_readonly_fields = ('name', 'type', 'display_websites', 'sftpuser', 'target_server')
    search_fields = ('name', 'account__username', 'data', 'website__domains__name')
    list_prefetch_related = ('content_set__website', 'content_set__website__domains')
    plugin = AppType
    plugin_field = 'type'
    plugin_title = _("Web application type")
    actions = (list_accounts,)

    display_type = display_plugin_field('type')


    @mark_safe
    def display_websites(self, webapp):
        websites = []
        for content in webapp.content_set.all():
            site_url = content.get_absolute_url()
            site_link = get_on_site_link(site_url)
            website = content.website
            #name = "%s on %s %s" % (website.name, content.path, site_link)
            name = "%s on %s" % (website.name, content.path)
            link = admin_link(display=name)(website)
            websites.append(link)
        if not websites:
            add_url = reverse('admin:websites_website_add')
            add_url += '?account=%s' % webapp.account_id
            plus = '<strong style="color:green; font-size:12px">+</strong>'
            websites.append('<a href="%s">%s%s</a>' % (add_url, plus, gettext("Add website")))
        return '<br>'.join(websites)
    display_websites.short_description = _("web sites")

    def display_detail(self, webapp):
        try:
            return webapp.type_instance.get_detail()
        except KeyError:
            return mark_safe("<span style='color:red;'>Not available</span>")
    display_detail.short_description = _("detail")


admin.site.register(WebApp, WebAppAdmin)
