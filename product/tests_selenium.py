from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from selenium import webdriver
from selenium.webdriver.common.by import By

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
    
    def test_restricciones_no_admin(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_username").send_keys("Usuario2")
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario2PasswordJQSA!=")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.get(f'{self.live_server_url}/product/list')
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".padding-list:nth-child(4) .w-100")
        assert len(elements) == 0
        self.driver.get(f'{self.live_server_url}/product/report/list')
        text = self.driver.find_element(By.CSS_SELECTOR, ".col").text
        assert text != "Notificaciones de productos reportados"
        self.driver.get(f'{self.live_server_url}/product/show/55')
        elements = self.driver.find_elements(By.LINK_TEXT, "Editar")
        assert len(elements) == 0
        self.driver.get(f'{self.live_server_url}/product/review/46')
        assert self.driver.find_element(By.CSS_SELECTOR, ".mb-3").text == "Inicio de sesión"

    
    def test_restricciones_admin(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyAdminPasswordJQSA!=1")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.get(f'{self.live_server_url}/product/report/list')
        text = self.driver.find_element(By.CSS_SELECTOR, ".col").text
        assert len(text) > 0
        self.driver.get(f'{self.live_server_url}/product/review/46')
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".save")
        assert len(elements) > 0
        
        
        
    def test_admineditarproducto(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyAdminPasswordJQSA!=1")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.get(f'{self.live_server_url}/product/review/55')
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".save")
        assert len(elements) > 0