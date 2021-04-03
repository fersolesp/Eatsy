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

    def test_acceder(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.CSS_SELECTOR, ".col-sm-8").click()
        assert self.driver.title == "Eatsy - Productos"

    def test_add(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.CSS_SELECTOR, ".botonAdd > img").click()
        assert self.driver.title == "Eatsy - Añadir producto"
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.find_element(By.LINK_TEXT, "Cancelar").click()
        self.driver.switch_to.alert.accept()
        self.driver.find_element(By.ID, "menuNormal").click()
  

    def test_filtros(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.CSS_SELECTOR, ".col-auto > .w-100").click()
        self.driver.find_element(By.CSS_SELECTOR, ".modal-header").click()
        assert self.driver.title == "Eatsy - Productos"
        self.driver.find_element(By.ID, "id_orderBy").click()
        dropdown = self.driver.find_element(By.ID, "id_orderBy")
        dropdown.find_element(By.XPATH, "//option[. = 'Más baratos primero']").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        elements = self.driver.find_elements(By.ID, "dropdownMenuButton")
        assert len(elements) > 0
        self.driver.find_element(By.ID, "dropdownMenuButton").click()
  
      
    def test_nav(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.LINK_TEXT, "Mi cuenta").click()
        assert self.driver.find_element(By.LINK_TEXT, "Mi Perfil").text == "Mi Perfil"
        assert self.driver.find_element(By.LINK_TEXT, "Cerrar sesión").text == "Cerrar sesión"
        self.driver.find_element(By.LINK_TEXT, "Lista de productos").click()
        self.driver.find_element(By.CSS_SELECTOR, ".col-sm-8").click()
        assert self.driver.title == "Eatsy - Productos"
        self.driver.find_element(By.ID, "menuNormal").click()

    def test_show(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.LINK_TEXT, "Ver detalles").click()
        self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(1) > .row > .titulito").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".col-sm-4:nth-child(1) > .m-auto")
        assert len(elements) > 0
        self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(1) > .row > .titulito").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(1) > .row > .titulito").text == "Dietas:"
        self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(3) > .mb-2 > .titulito").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(3) > .mb-2 > .titulito").text == "   Descripción:"
        self.driver.find_element(By.CSS_SELECTOR, ".mt-3 > .titulito").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".mt-3 > .titulito").text == "   Precio medio: 3,69€"
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".mb-5 > .col-auto > .btn")
        assert len(elements) > 0
        self.driver.find_element(By.CSS_SELECTOR, ".mb-5 > .col-auto > .btn").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".mb-5 > .col-auto > .btn")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element, 0, 0).perform()
        self.driver.find_element(By.ID, "modalReportLabel").click()
        assert self.driver.title == "Eatsy - Detalles de producto"
        self.driver.find_element(By.CSS_SELECTOR, ".modal-footer:nth-child(2) > .btn-secondary").click()
        self.driver.find_element(By.CSS_SELECTOR, ".col-sm-4:nth-child(2) > .m-auto").click()
        self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(1) > .col-auto > .btn").click()
        self.driver.find_element(By.CSS_SELECTOR, "#modalComentar .modal-header").click()
        assert self.driver.title == "Eatsy - Detalles de producto"
        self.driver.find_element(By.ID, "id_titulo").click()
        self.driver.find_element(By.ID, "id_titulo").send_keys("prueba")
        self.driver.find_element(By.ID, "id_mensaje").click()
        self.driver.find_element(By.ID, "id_mensaje").send_keys("prueba ")
        self.driver.find_element(By.NAME, "commentButton").click()
        self.driver.find_element(By.CSS_SELECTOR, ".col-sm-4:nth-child(2) > .m-auto").click()
        self.driver.find_element(By.CSS_SELECTOR, ".product-card-comment > .titulito").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".product-card-comment > .titulito").text == "prueba"
        self.driver.find_element(By.CSS_SELECTOR, ".col-sm-4:nth-child(3) > .m-auto").click()
        self.driver.find_element(By.ID, "select").click()
        self.driver.find_element(By.ID, "select").click()
        elements = self.driver.find_elements(By.ID, "addUbicacion")
        assert len(elements) > 0
        self.driver.find_element(By.ID, "addUbicacion").click()
        elements = self.driver.find_elements(By.NAME, "addingUbication")
        assert len(elements) > 0
        self.driver.find_element(By.ID, "menuNormal").click()
    
    def test_unirse(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.LINK_TEXT, "Unirse").click()
        self.driver.find_element(By.CSS_SELECTOR, ".titleblock").click()
        self.driver.find_element(By.CSS_SELECTOR, ".imgheader").click()
  
    def test_admin(self):
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
        self.driver.find_element(By.CSS_SELECTOR, ".padding-list:nth-child(4) .w-100").click()
        self.driver.find_element(By.CSS_SELECTOR, "#modalEstado .modal-header").click()
        assert self.driver.title == "Eatsy - Productos"
        self.driver.find_element(By.CSS_SELECTOR, "#modalEstado .btn-secondary").click()
        self.driver.find_element(By.LINK_TEXT, "Revisar reportes").click()
        self.driver.find_element(By.CSS_SELECTOR, ".tituloReporte").click()
        assert self.driver.title == "Eatsy - Reportes"
        self.driver.find_element(By.ID, "menuNormal").click()
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.CSS_SELECTOR, ".col-lg-4:nth-child(2) .row-fluid:nth-child(4) .m-auto").click()
        elements = self.driver.find_elements(By.LINK_TEXT, "Editar")
        self.driver.find_element(By.LINK_TEXT, "Editar").click()
        self.driver.find_element(By.CSS_SELECTOR, "h3").click()
        assert self.driver.title == "Eatsy - Revisar"
        self.driver.find_element(By.LINK_TEXT, "Cancelar").click()
        self.driver.switch_to.alert.accept()
        self.driver.find_element(By.ID, "menuNormal").click()