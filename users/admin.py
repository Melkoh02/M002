from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'birth_date',
    )
    search_fields = (
        'name',
        'description',
        'birth_date',
    )
