from django.contrib import admin
from .models import BankDetails


@admin.register(BankDetails)
class BankDetailsAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "kind",
        "brand",
        "masked_value",
        "bank_code",
        "bank_name",
        "bank_name_source",
        "alias",
        "is_public",
        "updated_at",
    )
    list_filter = ("kind", "brand", "is_public", "bank_name_source", "bank_name")
    search_fields = (
        "owner__email",
        "owner__display_name",
        "bank_name",
        "alias",
    )
    autocomplete_fields = ("owner",)
    readonly_fields = ("created_at", "updated_at", "masked_value", "bank_code", "brand")
    fieldsets = (
        (None, {"fields": ("owner", "kind", "value", "alias")}),
        ("Card/CLABE meta", {"fields": ("brand", "bank_code")}),
        ("Bank info", {"fields": ("bank_name", "bank_name_source")}),
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
