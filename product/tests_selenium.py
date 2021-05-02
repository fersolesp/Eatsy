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

    def iniciar_sesion(self,username,password):
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_username").send_keys(username)
        self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
        self.driver.find_element(By.ID, "id_password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()

    def test_restriccionesadmin(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        self.iniciar_sesion("Usuario2","eatsyUsuario2PasswordJQSA!=")
        self.driver.get(f'{self.live_server_url}/product/list')
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".padding-list:nth-child(4) .w-100")
        assert len(elements) == 0
        self.driver.get(f'{self.live_server_url}/product/report/list')
        text = self.driver.find_element(By.CSS_SELECTOR, ".col").text
        assert text != "Notificaciones de productos reportados"
        self.driver.get(f'{self.live_server_url}/product/show/55')
        elements = self.driver.find_elements(By.LINK_TEXT, "Editar")
        assert len(elements) == 0

    def test_admineditarproducto(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        self.iniciar_sesion("admin","eatsyAdminPasswordJQSA!=1")
        self.driver.get(f'{self.live_server_url}/product/review/55')
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".save")
        assert len(elements) > 0

    def test_receta_e_ingredientes(self):
        self.driver.get(f'{self.live_server_url}/')
        self.iniciar_sesion("Usuario1","eatsyUsuario1PasswordJQSA!=")
        self.driver.get(f'{self.live_server_url}/product/show/32') 
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".nombreProducto")
        assert len(elements) > 0 
        self.driver.get(f'{self.live_server_url}/recipe/show/6')
        elements = self.driver.find_elements(By.XPATH, "//div[2]/div/div")
        assert len(elements) > 0
        self.driver.get(f'{self.live_server_url}/product/show/13') 
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".nombreProducto")
        assert len(elements) > 0

    def test_receta_e_ingredientes_no_registrado(self):
        self.driver.get(f'{self.live_server_url}/')
        elements = self.driver.find_elements(By.LINK_TEXT, "Iniciar sesión")
        assert len(elements) > 0
        self.driver.get(f'{self.live_server_url}/recipe/show/6')
        elements = self.driver.find_elements(By.XPATH, "//button[contains(.,\'Iniciar sesión\')]")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "Tofu")
        assert len(elements) == 0

    def test_aboutUs(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.CSS_SELECTOR, ".col-sm-2:nth-child(1) u").click()
        self.driver.find_element(By.CSS_SELECTOR, ".titleblock").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".titleblock").text == "¡Nuestro proyecto!"

    def test_contactUs(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.CSS_SELECTOR, ".col-sm-2:nth-child(2) u").click()
        self.driver.find_element(By.CSS_SELECTOR, ".titleblock").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".titleblock").text == "¡Contáctanos!"

    def test_privacy(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.find_element(By.CSS_SELECTOR, ".col-sm-3 u").click()
        self.driver.find_element(By.CSS_SELECTOR, ".titleblock").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".titleblock").text == "Políticas de privacidad"

    def test_listado_no_login(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        self.driver.get(f'{self.live_server_url}/product/list')
        assert self.driver.find_element(By.CSS_SELECTOR, ".mb-3").text == "Inicio de sesión"

    def test_listado_usuario_no_activo(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        self.iniciar_sesion("Usuario3","eatsyUsuario3PasswordJQSA!=")
        self.driver.get(f'{self.live_server_url}/product/list')
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".nombreProducto")
        assert len(elements) > 0


    def test_añadir_producto_no_login(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        self.driver.get(f'{self.live_server_url}/product/create')
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".mb-3")
        assert len(elements) > 0


    def test_añadir_producto_usuario_no_activo(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        self.iniciar_sesion("Usuario3","eatsyUsuario3PasswordJQSA!=")
        self.driver.get(f'{self.live_server_url}/product/create')
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".nombreProducto")
        assert len(elements) > 0

    def test_listado_usuario_activo(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        # INICIO DE SESIÓN
        self.iniciar_sesion("Usuario1","eatsyUsuario1PasswordJQSA!=")
        self.driver.get(f'{self.live_server_url}/product/list')
        # EXISTEN LAS CARDS
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".product-card-inner")
        assert len(elements) > 0
        self.driver.get(f'{self.live_server_url}/product/list?page=2')
        # EXISTEN LAS CARDS EN LA PG 2
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".product-card-inner")
        assert len(elements) > 0
        self.driver.get(f'{self.live_server_url}/product/list')
        self.driver.get(f'{self.live_server_url}/product/list?titulo=Natillas&dietas=3&orderBy=newest')
        # EXISTEN LAS CARDS PARA UN DADO NOMBRE BUSCADO
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".product-card-inner")
        assert len(elements) > 0

    def test_listado_admin(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        # INICIO DE SESIÓN
        self.iniciar_sesion("admin","eatsyAdminPasswordJQSA!=1")
        self.driver.get(f'{self.live_server_url}/product/list')
        # EXISTEN LAS CARDS
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".product-card-inner")
        assert len(elements) > 0
        self.driver.get(f'{self.live_server_url}/product/list?page=2')
        # EXISTEN LAS CARDS EN LA PG 2
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".product-card-inner")
        assert len(elements) > 0
        self.driver.get(f'{self.live_server_url}/product/list?estado=pendiente')
        self.driver.get(f'{self.live_server_url}/product/list?titulo=Natillas&dietas=3&orderBy=newest')
        # EXISTEN LAS CARDS PARA UN DADO NOMBRE BUSCADO
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".product-card-inner")
        assert len(elements) > 0
