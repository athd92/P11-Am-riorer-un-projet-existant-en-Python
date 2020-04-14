from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from ..views import homepage, register, logout_request, login_request
from ..views import aliments, account, infos, save_aliment, saved, delete
from ..views import alternative

# Create your tests here.


class TestUrl(SimpleTestCase):
    """Calss used to test the uls"""

    def test_homepage_is_resolved(self):
        url = reverse("main:homepage")
        print(resolve(url))
        self.assertEquals(resolve(url).func, homepage)

    def test_register_is_resolved(self):
        url = reverse("main:register")
        print(resolve(url))
        self.assertEquals(resolve(url).func, register)

    def test_logout_is_resolved(self):
        url = reverse("main:logout")
        print(resolve(url))
        self.assertEquals(resolve(url).func, logout_request)

    def test_login_is_resolved(self):
        url = reverse("main:login")
        print(resolve(url))
        self.assertEquals(resolve(url).func, login_request)

    def test_aliments_is_resolved(self):
        url = reverse("main:aliments")
        print(resolve(url))
        self.assertEquals(resolve(url).func, aliments)

    def test_account_is_resolved(self):
        url = reverse("main:account")
        print(resolve(url))
        self.assertEquals(resolve(url).func, account)

    def test_infos_is_resolved(self):
        url = reverse("main:infos", args=["1"])
        print(resolve(url))
        self.assertEquals(resolve(url).func, infos)

    def test_save_aliment_is_resolved(self):
        url = reverse("main:save_aliment", args=["1"])
        print(resolve(url))
        self.assertEquals(resolve(url).func, save_aliment)

    def test_saved_is_resolved(self):
        url = reverse("main:saved")
        print(resolve(url))
        self.assertEquals(resolve(url).func, saved)

    def test_delete_is_resolved(self):
        url = reverse("main:delete", args=["1"])
        print(resolve(url))
        self.assertEquals(resolve(url).func, delete)

    def test_alternative_is_resolved(self):
        url = reverse("main:alternative", args=["1"])
        print(resolve(url))
        self.assertEquals(resolve(url).func, alternative)

