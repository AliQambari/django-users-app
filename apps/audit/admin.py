from django.contrib import admin
from .models import LoginAudit

@admin.register(LoginAudit)
class LoginAuditAdmin(admin.ModelAdmin):
    list_display = ("user", "ip_address", "country", "timestamp")
    search_fields = ("user__username", "ip_address", "country")
    list_filter = ("country", "timestamp")
