from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.catalogo, name="catalogo"),
    path("producto/<int:id>/", views.detalle_producto, name="detalle_producto"),
]
