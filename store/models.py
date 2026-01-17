from django.db import models


class Category(models.Model):
    GENERO_CHOICES = [
        ('DAMA', 'Dama'),
        ('HOMBRE', 'Hombre'),
        ('NINO', 'Niño'),
    ]

    TIPO_CHOICES = [
        ('CAMISETA', 'Camiseta'),
        ('SUDADERA', 'Sudadera'),
        ('PANTALONETA', 'Pantaloneta'),
    ]

    genero = models.CharField("Género", max_length=10, choices=GENERO_CHOICES)
    tipo_producto = models.CharField("Tipo de producto", max_length=15, choices=TIPO_CHOICES)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return f"{self.get_tipo_producto_display()} - {self.get_genero_display()}"


class Product(models.Model):
    nombre = models.CharField("Nombre", max_length=200)
    categoria = models.ForeignKey(Category, verbose_name="Categoría", on_delete=models.CASCADE)
    descripcion = models.TextField("Descripción", blank=True)
    precio = models.PositiveIntegerField("Precio (COP)")
    activo = models.BooleanField("Activo", default=True)
    creado = models.DateTimeField("Creado", auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre


class Size(models.Model):
    nombre = models.CharField("Talla", max_length=10)

    class Meta:
        verbose_name = "Talla"
        verbose_name_plural = "Tallas"

    def __str__(self):
        return self.nombre


class ProductStock(models.Model):
    producto = models.ForeignKey(Product, verbose_name="Producto", on_delete=models.CASCADE)
    talla = models.ForeignKey(Size, verbose_name="Talla", on_delete=models.CASCADE)
    stock = models.PositiveIntegerField("Stock", default=0)
    unique_together = ("producto", "talla")



    class Meta:
        verbose_name = "Stock por talla"
        verbose_name_plural = "Stock por talla"
        unique_together = ("producto", "talla")

    def __str__(self):
        return f"{self.producto} - {self.talla}"


class ProductImage(models.Model):
    producto = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="imagenes",
        verbose_name="Producto"
    )
    imagen = models.ImageField("Imagen", upload_to="productos/")
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Foto de producto"
        verbose_name_plural = "Fotos de producto"
        ordering = ["orden", "id"]

    def __str__(self):
        return f"Foto - {self.producto.nombre}"


class SiteSettings(models.Model):
    texto_marca = models.TextField("Texto de marca (calidad / edición limitada)", blank=True, default="")
    terminos_html = models.TextField("Términos y condiciones (texto)", blank=True, default="")

    nombre_marca = models.CharField("Nombre de la marca", max_length=120, default="Betel Casa de Dios")
    ciudad_base = models.CharField("Ciudad base", max_length=120, default="Turbo, Antioquía")

    whatsapp_numero = models.CharField("WhatsApp (solo números, con indicativo)", max_length=20, default="573001099123")
    horario_atencion = models.CharField("Horario de atención", max_length=120, default="24/7")

    dias_produccion = models.CharField("Tiempo de producción", max_length=120, default="3 días")
    envio_tiempo = models.CharField("Tiempo de envío", max_length=120, default="3 a 5 días hábiles (según ciudad)")
    envio_nota = models.TextField("Nota de envío", blank=True, default="Envío con transportadora (uso exclusivo).")

    politicas_no_devolucion = models.TextField(
        "Política (no devoluciones)",
        default="No realizamos devoluciones por talla o gusto. Marca 100% online, no contamos con tienda física."
    )
    excepcion_falla = models.TextField(
        "Excepción por falla",
        default="Única excepción: falla de estampado. Se reporta máximo 1–2 días después de entregado."
    )

    logo = models.ImageField("Logo (opcional)", upload_to="branding/", blank=True, null=True)

    class Meta:
        verbose_name = "Ajustes del sitio"
        verbose_name_plural = "Ajustes del sitio"

    def __str__(self):
        return "Ajustes del sitio"
