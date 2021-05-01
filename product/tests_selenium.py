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
    
    # def test_noactivo(self):
    #     self.driver.get(f'{self.live_server_url}/')
    #     elements = self.driver.find_elements(By.LINK_TEXT, "Iniciar sesión")
    #     assert len(elements) > 0
    #     elements = self.driver.find_elements(By.LINK_TEXT, "Registrarse")
    #     assert len(elements) > 0
    #     self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
    #     self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #     self.driver.find_element(By.ID, "id_username").send_keys("Usuario3")
    #     self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #     self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario3PasswordJQSA!")
    #     self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario3PasswordJQSA!=")
    #     self.driver.find_element(By.CSS_SELECTOR, ".save").click()
    #     elements = self.driver.find_elements(By.LINK_TEXT, "Activa tu cuenta")
    #     elements = self.driver.find_elements(By.CSS_SELECTOR, ".save")
    #     assert len(elements) > 0
    #     elements = self.driver.find_elements(By.CSS_SELECTOR, ".col-auto > .btn:nth-child(2)")
    #     assert len(elements) > 0
    #     self.driver.get(f'{self.live_server_url}/product/list')
    #     elements = self.driver.find_elements(By.CSS_SELECTOR, ".mt-3")
        
    # def test_activ(self):
    #     self.driver.get(f'{self.live_server_url}/')
    #     self.driver.set_window_size(1080, 1036)
    #     self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
    #     self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #     self.driver.find_element(By.ID, "id_username").send_keys("Usuario2")
    #     self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #     self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario2PasswordJQSA!=")
    #     self.driver.find_element(By.CSS_SELECTOR, ".save").click()
    #     self.driver.get(f'{self.live_server_url}/product/list')
    #     assert self.driver.find_element(By.CSS_SELECTOR, ".col-sm-8").text == "Búsqueda de productos"

    def test_restriccionesadmin(self):
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
    
    # def test_addubi(self):
    #     self.driver.get(f'{self.live_server_url}/')
    #     self.driver.set_window_size(1080, 1036)
    #     self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
    #     self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #     self.driver.find_element(By.ID, "id_username").send_keys("Usuario2")
    #     self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #     self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario2PasswordJQSA!=")
    #     self.driver.find_element(By.CSS_SELECTOR, ".save").click()
    #     self.driver.get(f'{self.live_server_url}/product/show/55')
    #     self.driver.find_element(By.XPATH, "//div[@id=\'collapseproducts\']/div[3]/span").click()
    #     self.driver.find_element(By.ID, "addUbicacion").click()
    #     self.driver.find_element(By.ID, "id_ubicaciones").click()
    #     dropdown = self.driver.find_element(By.ID, "id_ubicaciones")
    #     dropdown.find_element(By.XPATH, "//option[. = 'Lidl']").click()
    #     self.driver.find_element(By.ID, "id_ubicaciones").click()
    #     self.driver.find_element(By.ID, "id_precio").click()
    #     self.driver.find_element(By.ID, "id_precio").send_keys("2")
    #     self.driver.find_element(By.NAME, "addingUbication").click()
    #     self.driver.find_element(By.CSS_SELECTOR, ".col-sm-4:nth-child(3) > .m-auto").click()
    #     self.driver.find_element(By.ID, "select").click()
    #     dropdown = self.driver.find_element(By.ID, "select")
    #     dropdown.find_element(By.XPATH, "//option[. = 'Lidl']").click()

    #   TODO test que falla para arreglar
    # def test_reportar(self):
    #     self.driver.get(f'{self.live_server_url}/')
    #     self.driver.set_window_size(1080, 1036)
    #     self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
    #     self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #     self.driver.find_element(By.ID, "id_username").send_keys("Usuario2")
    #     self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #     self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario2PasswordJQSA!=")
    #     self.driver.find_element(By.CSS_SELECTOR, ".save").click()
    #     self.driver.get(f'{self.live_server_url}/product/show/55')
    #     elements = self.driver.find_elements(By.CSS_SELECTOR, ".mb-5 > .col-auto > .btn")
    #     assert len(elements) > 0
    #     self.driver.find_element(By.CSS_SELECTOR, ".mb-5 > .col-auto > .btn").click()
    #     elements = self.driver.find_elements(By.NAME, "reportButton")

    #def test_selenium_paginacion(self):
    #    self.driver.get(f'{self.live_server_url}/')
    #    self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
    #    self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #    self.driver.find_element(By.ID, "id_username").send_keys("Usuario1")
    #    self.driver.find_element(By.CSS_SELECTOR, ".container > .row").click()
    #    self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
    #    self.driver.find_element(By.CSS_SELECTOR, ".save").click()
    #    self.driver.find_element(By.CSS_SELECTOR, ".col-xl-3:nth-child(12) .descripcion").click()
    #    self.driver.find_element(By.ID, "pglink2").click()
    #    self.driver.find_element(By.CSS_SELECTOR, ".col-xl-3:nth-child(12) > .product-card-inner").click()

    #def test_selenium_create_product(self):
    #    self.driver.get(f'{self.live_server_url}/')
    #    self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
    #    self.driver.find_element(By.ID, "id_username").send_keys("Usuario1")
    #    self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
    #    self.driver.find_element(By.CSS_SELECTOR, ".save").click()
    #    self.driver.find_element(By.CSS_SELECTOR, ".botonAdd > img").click()
    #    #self.driver.find_element(By.ID, "id_foto").send_keys("\leche.jpg")
    #    self.driver.find_element(By.ID, "id_nombre").send_keys("ProductoEjemplo")
    #    self.driver.find_element(By.ID, "id_descripcion").send_keys("Un producto de ejemplo")
    #    self.driver.find_element(By.ID, "id_precio").send_keys("1.99")
    #    dropdown = self.driver.find_element(By.ID, "id_dieta")
    #    dropdown.find_element(By.XPATH, "//option[. = 'Vegetariano']").click()
    #    self.driver.find_element(By.ID, "id_ubicaciones").click()
    #    dropdown = self.driver.find_element(By.ID, "id_ubicaciones")
    #    dropdown.find_element(By.XPATH, "//option[. = 'Carrefour']").click()
    #    elements = self.driver.find_elements(By.CSS_SELECTOR, ".save")
    #    assert len(elements) > 0
    #    self.driver.find_element(By.CSS_SELECTOR, ".save").click()

    #def test_selenium_not_create_product(self):
    #    self.driver.get(f'{self.live_server_url}/')
    #    self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
    #    self.driver.find_element(By.ID, "id_username").send_keys("Usuario1")
    #    self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
    #    self.driver.find_element(By.CSS_SELECTOR, ".save").click()
    #    self.driver.find_element(By.CSS_SELECTOR, ".botonAdd > img").click()
    #    #self.driver.find_element(By.ID, "id_foto").send_keys("\leche.jpg")
    #    self.driver.find_element(By.ID, "id_nombre").send_keys("ProductoMalEjemplo")
    #    self.driver.find_element(By.ID, "id_descripcion").click()
    #    self.driver.find_element(By.ID, "id_descripcion").send_keys("Un producto de mal ejemplo")
    #    self.driver.find_element(By.ID, "id_precio").send_keys("100.01")
    #    dropdown = self.driver.find_element(By.ID, "id_dieta")
    #    dropdown.find_element(By.XPATH, "//option[. = 'Vegetariano']").click()
    #    dropdown.find_element(By.XPATH, "//option[. = 'Vegano']").click()
    #    elements = self.driver.find_elements(By.CSS_SELECTOR, ".col-sm-8")
    #    assert len(elements) > 0

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
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("Usuario3")
        self.driver.find_element(By.ID, "id_password").click()
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario3PasswordJQSA!=")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
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
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("Usuario3")
        self.driver.find_element(By.ID, "id_password").click()
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario3PasswordJQSA!=")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
        self.driver.get(f'{self.live_server_url}/product/create')
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".nombreProducto")
        assert len(elements) > 0
    

    def test_listado_usuario_activo(self):
        self.driver.get(f'{self.live_server_url}/')
        self.driver.set_window_size(1080, 1036)
        # INICIO DE SESIÓN
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("Usuario1")
        self.driver.find_element(By.ID, "id_password").click()
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyUsuario1PasswordJQSA!=")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
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
        self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").click()
        self.driver.find_element(By.ID, "id_password").send_keys("eatsyAdminPasswordJQSA!=1")
        self.driver.find_element(By.CSS_SELECTOR, ".save").click()
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

    
    # def test_pruebaCreacion(self):
    #     self.driver.get(f'{self.live_server_url}/')
    #     self.driver.set_window_size(1080, 1036)
    #     # INICIO DE SESIÓN
    #     self.driver.find_element(By.LINK_TEXT, "Iniciar sesión").click()
    #     self.driver.find_element(By.ID, "id_username").click()
    #     self.driver.find_element(By.ID, "id_username").send_keys("admin")
    #     self.driver.find_element(By.ID, "id_password").click()
    #     self.driver.find_element(By.ID, "id_password").send_keys("eatsyAdminPasswordJQSA!=1")
    #     self.driver.find_element(By.CSS_SELECTOR, ".save").click()
    #     self.driver.find_element(By.CSS_SELECTOR, "#botonAdd > img").click()
    #     # AÑADIR PRODUCTO
    #     self.driver.find_element(By.CSS_SELECTOR, ".col-md-3").click()
    #     self.driver.find_element(By.ID, "id_foto").send_keys("C:/Users/nekom/Desktop/Pablo/Universidad/4º Carrera/SSII/ASIT/CAI/CAI-4/Imagenes/Fichero4.png")
    #     self.driver.find_element(By.ID, "id_nombre").click()
    #     self.driver.find_element(By.ID, "id_nombre").send_keys("Prueba")
    #     self.driver.find_element(By.ID, "id_descripcion").click()
    #     self.driver.find_element(By.ID, "id_descripcion").send_keys("prueba")
    #     self.driver.find_element(By.ID, "id_precio").click()
    #     self.driver.find_element(By.ID, "id_precio").send_keys("5")
    #     dropdown = self.driver.find_element(By.ID, "id_dieta")
    #     dropdown.find_element(By.XPATH, "//option[. = 'Vegetariano']").click()
    #     dropdown = self.driver.find_element(By.ID, "id_dieta")
    #     dropdown.find_element(By.XPATH, "//option[. = 'Sin gluten']").click()
    #     self.driver.find_element(By.ID, "id_ubicaciones").click()
    #     dropdown = self.driver.find_element(By.ID, "id_ubicaciones")
    #     dropdown.find_element(By.XPATH, "//option[. = 'Lo Vegano']").click()
    #     self.driver.find_element(By.ID, "id_ubicaciones").click()
    #     self.driver.find_element(By.CSS_SELECTOR, ".save").click()
    #     # BUSCAR PRODCUTO RECIEN AÑADIDO COMO PENDIENTE
    #     self.driver.find_element(By.ID, "dropdownMenuButton").click()
    #     self.driver.find_element(By.ID, "id_titulo").click()
    #     self.driver.get(f'{self.live_server_url}/product/list?titulo=Prueba&orderBy=newest&estado=pendiente')
    #     elements = self.driver.find_elements(By.CSS_SELECTOR, ".col-sm-8")
    #     assert len(elements) > 0
    #     elements = self.driver.find_elements(By.CSS_SELECTOR, ".product-card-inner")
    #     assert len(elements) > 0