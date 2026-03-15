from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Re-register the built-in User model with the full UserAdmin interface
# so username, email, permissions, groups, etc. are all visible in the admin.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
