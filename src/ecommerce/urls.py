from django.urls import path
from django.contrib.auth.views import LoginView
from ecommerce import views

urlpatterns = [
    path("my-products/", views.ProtectedListView.as_view(), name="my-products"),
    path(
        "login/",
        LoginView.as_view(
            template_name="ecommerce/login.html",
            next_page="my-products",
        ),
        name="ecommerce-login",
    ),
    path("", views.product_model_list_view, name='product-list'),  # Lista de productos
    path("product/<int:pk>/", views.product_model_detail_view, name='product-detail'),  # Detalle de un producto
    path("product/create/", views.product_model_create_view, name='product-create'),  # Crear un producto
    path("product/<int:pk>/update/", views.product_model_update_view, name='product-update'),  # Actualizar un producto
    path("product/<int:pk>/delete/", views.product_model_delete_view, name='product-delete'),  # Eliminar un producto
]
