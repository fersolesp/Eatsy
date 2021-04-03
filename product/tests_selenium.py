import json
import pytest
import time
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


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

    def test_unirse(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.LINK_TEXT, "Unirse").click()
        self.driver.find_element(By.CSS_SELECTOR, ".titleblock").click()
        self.driver.find_element(By.CSS_SELECTOR, ".imgheader").click()

    def test_admin_revisar(self):
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element(By.CSS_SELECTOR, ".login").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.CSS_SELECTOR, ".login").click()
        self.driver.find_element(By.CSS_SELECTOR, ".login").click()
        self.driver.find_element(By.ID, "id_password").send_keys("admin")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-row > input").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2)").click()
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        elements = self.driver.find_elements(By.LINK_TEXT, "Revisar reportes")

    def test_add(self):
        self.driver.get(f'{self.live_server_url}/product/create')
        assert self.driver.find_element_by_text(u"Añadir un producto").text == u"Añadir un producto"
        assert self.driver.title == "Añadir un producto"
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.find_element(By.LINK_TEXT, "Cancelar").click()
        self.driver.switch_to.alert.accept()
        self.driver.find_element(By.ID, "menuNormal").click()
  

    def test_filtros(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Filtros\')]").click()
        assert self.driver.find_element(By.ID, "modalComentarLabel").text == "Aplicar filtros y ordenar los productos"
        self.driver.find_element(By.CSS_SELECTOR, "#modalComentar .btn-secondary").click()
  
      
    def test_nav(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        elements = self.driver.find_elements(By.LINK_TEXT, "Mi cuenta")
        elements = self.driver.find_elements(By.LINK_TEXT, "Lista de productos")

    def test_show(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.CSS_SELECTOR, ".col-lg-4:nth-child(2) .row-fluid:nth-child(4) .m-auto").click()
        self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(1) > .mb-2").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(1) > .row > .titulito").text == "Dietas:"
        self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(3) > .mb-2").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(3) > .mb-2 > .titulito").text == "   Descripción:"



