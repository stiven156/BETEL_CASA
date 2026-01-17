from django.shortcuts import render, get_object_or_404
from .models import Product, SiteSettings


def catalogo(request):
    ajustes = SiteSettings.objects.first()

    genero = (request.GET.get("genero") or "").upper()
    tipo = (request.GET.get("tipo") or "").upper()

    productos = Product.objects.filter(activo=True).select_related("categoria").order_by("-creado")

    if genero:
        productos = productos.filter(categoria__genero=genero)
    if tipo:
        productos = productos.filter(categoria__tipo_producto=tipo)

    generos = [
        ("HOMBRE", "Hombre"),
        ("DAMA", "Dama"),
        ("NINO", "Niño"),
    ]
    tipos = [
        ("CAMISETA", "Camisetas"),
        ("SUDADERA", "Sudaderas"),
        ("PANTALONETA", "Pantalonetas"),
    ]

    return render(request, "store/catalogo.html", {
        "ajustes": ajustes,
        "productos": productos,
        "genero": genero,
        "tipo": tipo,
        "generos": generos,
        "tipos": tipos,
    })


def detalle_producto(request, id):
    ajustes = SiteSettings.objects.first()
    producto = get_object_or_404(Product, id=id, activo=True)

    tallas = producto.productstock_set.filter(stock__gt=0).select_related("talla").order_by("talla__nombre")
    fotos = producto.imagenes.all()

    return render(request, "store/detalle_producto.html", {
        "ajustes": ajustes,
        "producto": producto,
        "tallas": tallas,
        "fotos": fotos,
    })
