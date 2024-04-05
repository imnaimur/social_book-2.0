from django.contrib import admin
from .models import CustomUser,Post
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_name",'is_active','is_superuser','is_staff')
admin.site.register(CustomUser,UserAdmin)
admin.site.register(Post)
