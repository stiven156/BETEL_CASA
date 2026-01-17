from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, Size, ProductStock, ProductImage, SiteSettings


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("tipo_producto", "genero")
    list_filter = ("tipo_producto", "genero")
    search_fields = ("tipo_producto", "genero")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ("imagen", "orden")


class ProductStockInline(admin.TabularInline):
    model = ProductStock
    extra = 0
    fields = ("talla", "stock")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("miniatura", "nombre", "categoria", "precio_cop", "activo", "creado")
    list_filter = ("activo", "categoria")
    search_fields = ("nombre", "descripcion")
    list_editable = ("activo",)
    inlines = [ProductImageInline, ProductStockInline]

    def miniatura(self, obj):
        primera = obj.imagenes.first()
        if primera and primera.imagen:
            return format_html(
                '<img src="{}" style="height:45px; border-radius:6px;" />',
                primera.imagen.url
            )
        return "—"
    miniatura.short_description = "Foto"

    def precio_cop(self, obj):
        return f"$ {obj.precio:,.0f}".replace(",", ".")
    precio_cop.short_description = "Precio"


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ("producto", "talla", "stock")
    list_filter = ("talla", "producto")
    search_fields = ("producto__nombre",)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='products/')



class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logo/')
    whatsapp = models.CharField(max_length=20)
