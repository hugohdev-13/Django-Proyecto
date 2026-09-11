from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ProductModel


class ProtectedProductsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="owner", password="test-password")
        cls.other = get_user_model().objects.create_user(username="other")
        cls.owned = ProductModel.objects.create(title="Mine", price=10, owner=cls.user)
        cls.foreign = ProductModel.objects.create(title="Other", price=20, owner=cls.other)
        cls.legacy = ProductModel.objects.create(title="Legacy", price=30)

    def test_anonymous_list_redirects_to_login(self):
        response = self.client.get(reverse("my-products"))
        self.assertRedirects(response, reverse("ecommerce-login") + "?next=" + reverse("my-products"))

    def test_list_only_contains_current_users_products(self):
        for user, product in [(self.user, self.owned), (self.other, self.foreign)]:
            self.client.force_login(user)
            response = self.client.get(reverse("my-products"))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "ecommerce/list-view.html")
            self.assertQuerySetEqual(response.context["products"], [product])

    def test_user_without_products_has_empty_list(self):
        user = get_user_model().objects.create_user(username="empty")
        self.client.force_login(user)
        response = self.client.get(reverse("my-products"))
        self.assertQuerySetEqual(response.context["products"], [])

    def test_anonymous_cannot_create_product(self):
        for method in [self.client.get, self.client.post]:
            response = method(reverse("product-create"), {"title": "Blocked", "price": "5"})
            self.assertEqual(response.status_code, 302)
        self.assertEqual(ProductModel.objects.count(), 3)

    def test_creation_uses_authenticated_user_even_if_owner_is_posted(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("product-create"), {
            "title": "Created", "price": "15", "owner": self.other.pk,
        })
        self.assertRedirects(response, reverse("product-list"))
        self.assertEqual(ProductModel.objects.get(title="Created").owner, self.user)

    def test_public_list_keeps_legacy_and_other_products(self):
        response = self.client.get(reverse("product-list"))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["products"], [self.owned, self.foreign, self.legacy])

    def test_regular_user_can_login_and_return_to_protected_list(self):
        response = self.client.post(reverse("ecommerce-login"), {
            "username": "owner", "password": "test-password", "next": reverse("my-products"),
        })
        self.assertRedirects(response, reverse("my-products"))

    def test_login_without_next_defaults_to_my_products(self):
        response = self.client.post(reverse("ecommerce-login"), {
            "username": "owner", "password": "test-password",
        })
        self.assertRedirects(response, reverse("my-products"))
