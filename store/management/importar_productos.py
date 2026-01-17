import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings

from store.models import Category, Product, Size, ProductStock, ProductImage


class Command(BaseCommand):
    help = "Importa productos desde un CSV + opcionalmente fotos desde una carpeta."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Ruta del archivo CSV (ej: data/productos.csv)")
        parser.add_argument(
            "--fotos_dir",
            type=str,
            default="",
            help="Carpeta donde están las fotos (ej: data/fotos). Si no se pasa, no carga fotos.",
        )

    def handle(self, *args, **options):
        csv_path = Path(options["csv_path"]).resolve()
        fotos_dir = Path(options["fotos_dir"]).resolve() if options["fotos_dir"] else None

        if not csv_path.exists():
            self.stderr.write(self.style.ERROR(f"No existe el CSV: {csv_path}"))
            return

        # Asegura MEDIA_ROOT
        Path(settings.MEDIA_ROOT).mkdir(parents=True, exist_ok=True)

        creados = 0
        actualizados = 0

        with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            required = ["nombre", "tipo_producto", "genero", "precio", "activo", "stock"]
            for r in required:
                if r not in reader.fieldnames:
                    self.stderr.write(self.style.ERROR(f"Falta columna obligatoria: {r}"))
                    self.stderr.write(self.style.WARNING(f"Columnas encontradas: {reader.fieldnames}"))
                    return

            for row in reader:
                nombre = row["nombre"].strip()
                tipo_producto = row["tipo_producto"].strip().upper()
                genero = row["genero"].strip().upper()
                precio = int(row["precio"].strip())
                activo = row["activo"].strip().lower() in ("1", "true", "si", "sí", "yes", "y")
                stock_str = row["stock"].strip()

                # Categoria
                categoria, _ = Category.objects.get_or_create(
                    tipo_producto=tipo_producto,
                    genero=genero,
                )

                # Producto (si existe por nombre+categoria, lo actualiza)
                producto, created = Product.objects.get_or_create(
                    nombre=nombre,
                    categoria=categoria,
                    defaults={"precio": precio, "activo": activo},
                )
                if created:
                    creados += 1
                else:
                    producto.precio = precio
                    producto.activo = activo
                    producto.save()
                    actualizados += 1

                # Stock por talla: formato "S:10|M:5|L:2"
                # Borra stock previo para “sync” perfecto
                ProductStock.objects.filter(producto=producto).delete()

                partes = [p.strip() for p in stock_str.split("|") if p.strip()]
                for p in partes:
                    talla_txt, cant_txt = [x.strip() for x in p.split(":")]
                    talla, _ = Size.objects.get_or_create(nombre=talla_txt)
                    ProductStock.objects.create(producto=producto, talla=talla, stock=int(cant_txt))

                # Fotos (opcional): columna "fotos" con "img1.jpg|img2.jpg|img3.jpg"
                # Solo si se pasa --fotos_dir y existe la columna
                if fotos_dir and "fotos" in row and row["fotos"].strip():
                    ProductImage.objects.filter(producto=producto).delete()
                    fotos = [x.strip() for x in row["fotos"].split("|") if x.strip()]
                    for idx, filename in enumerate(fotos):
                        file_path = (fotos_dir / filename).resolve()
                        if not file_path.exists():
                            self.stderr.write(self.style.WARNING(f"Foto no encontrada: {file_path} (producto: {nombre})"))
                            continue
                        with file_path.open("rb") as img_f:
                            pi = ProductImage(producto=producto, orden=idx)
                            pi.imagen.save(file_path.name, File(img_f), save=True)

        self.stdout.write(self.style.SUCCESS(f"Listo ✅ Creados: {creados} | Actualizados: {actualizados}"))
