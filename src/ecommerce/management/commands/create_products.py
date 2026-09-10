from django.core.management.base import BaseCommand

from ecommerce.models import ProductModel


class Command(BaseCommand):
    help = "Crea 500 productos de prueba utilizando bulk_create"

    def handle(self, *args, **options):
        products = []

        for i in range(1, 501):
            product = ProductModel(
                title=f"Producto de prueba {i}",
                price=round(10 + (i * 1.5), 2),
                description=f"Descripción del producto de prueba número {i}",
                seller=f"Vendedor {(i % 10) + 1}",
                color=["Rojo", "Azul", "Verde", "Negro", "Blanco"][i % 5],
                product_dimensions=f"{10 + (i % 20)}x{5 + (i % 10)}x{2 + (i % 5)} cm",
            )

            products.append(product)

        ProductModel.objects.bulk_create(products)

        self.stdout.write(
            self.style.SUCCESS(
                f"Se crearon correctamente {len(products)} productos."
            )
        )