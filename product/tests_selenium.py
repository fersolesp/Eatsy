import json
from django.utils import timezone
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command

class SeleniumTests(StaticLiveServerTestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1920, 1080)
        super().setUp()
        call_command("flush", interactive=False)
        call_command("loaddata", "datosEjemplo.json")

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        call_command("flush", interactive=False)


    def test_base_page(self):
        self.driver.get(f'{self.live_server_url}/')
        assert self.driver.find_element_by_link_text(u"Iniciar sesión").text == u"Iniciar sesión"