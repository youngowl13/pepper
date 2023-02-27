from django.contrib import admin
from users.models import User, Role


@admin.register(User)
@admin.register(Role)
class UserAdmin(admin.ModelAdmin):
    pass
