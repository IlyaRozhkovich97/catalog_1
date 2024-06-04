from django.db import models


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=100, verbose_name="наименование")
    description = models.CharField(max_length=255, verbose_name="описание")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    objects = None
    name = models.CharField(max_length=255, verbose_name="наименование")
    description = models.TextField(blank=True, null=True, verbose_name="описание")
    image = models.ImageField(upload_to="product/image", blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="категория",
        blank=True,
        null=True,
        related_name="products",
    )
    purchase_price = models.IntegerField(
        blank=True, null=True, verbose_name="цена продажи"
    )
    created_at = models.DateField(blank=True, null=True, verbose_name="дата создания")
    updated_at = models.DateField(
        blank=True, null=True, verbose_name="дата последнего изменения"
    )
    views_counter = models.PositiveIntegerField(
        default=0,
        verbose_name="количество просмотров",
        help_text="Укажите количество просмотров",
    )
    is_published = models.BooleanField(default=True, verbose_name="опубликован")
    slug = models.CharField(max_length=255, verbose_name="slug", null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.category}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "category", "purchase_price"]


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    version_number = models.CharField(max_length=100)
    version_name = models.CharField(max_length=100)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.version_name} ({self.version_number})"
