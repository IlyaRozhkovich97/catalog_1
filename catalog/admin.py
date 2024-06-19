from django.contrib import admin
from .models import Product, Version, Category


class VersionInline(admin.TabularInline):
    model = Version
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'purchase_price', 'created_at', 'updated_at', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('name', 'description')
    inlines = [VersionInline]

    fields = ('name', 'category', 'purchase_price', 'description', 'is_published')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
