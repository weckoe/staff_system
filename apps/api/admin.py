from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.filters import AllValuesFieldListFilter

from apps.api.models import User

from configuration.task import delete_salary_information_async


@admin.action(description='Delete salary information for this staff members')
def delete_salary_information(modeladmin, request, queryset):
    if len(queryset) < 20:
        queryset.update(salary_information=None)
    delete_salary_information_async.delay([user_id.id for user_id in queryset])


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'position',
        'hiring_date',
        'salary',
        'salary_information',
        'upper_manager_url',
    )

    list_filter = ['position', ('position', AllValuesFieldListFilter), ]

    actions = [delete_salary_information]

    def upper_manager_url(self, obj):
        if obj.head_manager == None:
            return format_html('<a>There is No Upper Manager</a>')

        url = (
                reverse('admin:api_user_changelist')
                + f'?position__exact={obj.head_manager.position}'
        )

        return format_html('<a href="{}">Upper Manager</a>', url)
