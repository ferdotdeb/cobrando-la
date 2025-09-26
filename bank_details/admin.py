from django.contrib import admin
from .models import BankDetails

@admin.register(BankDetails)
class BankDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'kind',
        'masked_value',
        'bank_name',
        'alias',
        'is_public',
        'updated_at'
    )
    list_filter = ('kind', 'is_public', 'bank_name')
    search_fields = (
        'owner__email',
        'owner__display_name',
        'owner__username',
        'bank_name',
        'alias',
    )
    autocomplete_fields = ('owner',)
    readonly_fields = ('created_at', 'updated_at', 'masked_value')
    fieldsets = (
        (None, {"fields": ("owner", "kind", "value", "bank_name", "alias")}),
        ("Visibility", {"fields": ("is_public",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
        ("Computed", {"fields": ("masked_value",)}),
    )

    actions = ("make_public", "make_private")

    @admin.action(description="Mark selected as PUBLIC")
    def make_public(self, request, queryset):
        queryset.update(is_public=True)

    @admin.action(description="Mark selected as PRIVATE")
    def make_private(self, request, queryset):
        queryset.update(is_public=False)
