from django.contrib import admin
from unfold.admin import ModelAdmin

# @admin.register(User) - треба User кастомний створити
class CustomAdminClass(ModelAdmin):
    pass