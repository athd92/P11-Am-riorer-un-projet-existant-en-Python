from selenium import webdriver
from main.models import Aliment
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time
from django.test import Client
from django.contrib.auth.models import User
from selenium.webdriver.support.ui import WebDriverWait


class TestAjaxSendMail(StaticLiveServerTestCase):
    """
    Class used to test ajax request with selenium
    """

    def setUp(self):

        self.browser = webdriver.Firefox()
        self.client = Client()
        self.client = User.objects.create_user(
            "usertest", "athd333@gmail.com", "Password3216854+"
        )
        self.aliment = Aliment.objects.create(
            name="Tomates",
            name_fr="Tomates cerises",
            date="2019/01/09",
            brands="La Conserve",
            nutriscore="a",
            ingredients="Tomates, sel, sure, conservateurs",
            image="https://image-test-p8-url-test.com",
            url="https://test-p8-url-test.com",
            stores="Lidl, Auchan, Franprix",
            quantity="200g",
            packaging="Conserve",
            ingredients_fr="Tomates, sel, sucre",
            manufactured_places="Dijon",
            purchase_places="Bordeaux, Paris",
            categories="Légumes",
            code="654f654651651",
        )

    def test_login_and_send_ajax(self):

        wait = WebDriverWait(self.browser, 30)
        # access login page
        self.browser.get(self.live_server_url + reverse("main:login"))
        username = self.browser.find_element_by_id("id_username")
        username.send_keys("usertest")
        password = self.browser.find_element_by_id("id_password")
        password.send_keys("Password3216854+")
        btn = self.browser.find_element_by_class_name("btn")
        btn.click()
        # redirect user to main page
        search_bar = self.browser.find_element_by_xpath('//*[@id="aliments"]')
        search_bar.send_keys("Tomates")
        submit_btn = self.browser.find_element_by_xpath(
            "/html/body/nav/div[2]/ul/li[1]/div/form/div/div/input"
        )
        submit_btn.click()

        infos = self.browser.find_element_by_id("getinfos")
        infos.click()
        time.sleep(5)
        print("LANCEMENT AJAX")
        mail = self.browser.find_element_by_id("mail")
        mail.click()
        wait.until(
            lambda browser: self.browser.execute_script(
                "return jQuery.active == 0"
            )
        )

