from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User


class AdminUser(UserAdmin):
	list_display = ("email", "username", "first_name","date_joined", "last_login","is_admin","is_staff")
	search_fields = ("email","username", "first_name")
	readonly_fields = ("date_joined", "last_login")

	filter_horizontal =()
	list_filter = ("is_admin", "is_staff","is_active")
	fieldsets = ()

admin.site.register(User, AdminUser)