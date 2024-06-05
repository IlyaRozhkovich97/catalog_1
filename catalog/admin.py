from django.contrib import admin
from catalog.models import Category, Product, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "purchase_price")
    list_filter = ("category",)
    search_fields = ("name",)

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "version_number", "version_name", "is_current")
    list_filter = ("product", "is_current")
    search_fields = ("version_name", "version_number")