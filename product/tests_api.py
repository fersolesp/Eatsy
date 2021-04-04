from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.core.management import call_command
from urllib.parse import urlencode
import json
from django.core.files.uploadedfile import SimpleUploadedFile
# Create your tests here.

class EatsyApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        call_command("collectstatic", interactive=False)
        call_command("flush", interactive=False)
        call_command("loaddata", "datosEjemplo.json")
        super().setUp()

    def tearDown(self):
        super().tearDown()
        # call_command("flush", interactive=False)

    def test_accessing_admin(self):
        data = {}
        self.client.login(username="admin", password="admin")
        response = self.client.get('/admin/product/producto/', data, format= 'json')
        self.assertEquals(response.status_code, 200)
        self.client.logout()

    def test_accessing_admin_302(self):
        data = {}
        response = self.client.get('/admin/product/producto/', data, format= 'json')
        self.assertEquals(response.status_code, 302)

    def test_main_page(self):
        response = self.client.get('/', {}, format= 'json')
        self.assertEquals(response.status_code, 200)

    def test_subscription_page(self):
        response = self.client.get('/subscribe/', {}, format= 'json')
        self.assertEquals(response.status_code, 200)

    def test_product_list(self):
        response = self.client.get('/product/list', {}, format= 'json')
        self.assertEquals(response.status_code, 200)

    def test_product_show(self):
        response = self.client.get('/product/show/24', {}, format= 'json')
        self.assertEquals(response.status_code, 200)

    def test_pending_product(self):
        response = self.client.get('/product/show/25', {}, format= 'json')
        self.assertEquals(response.status_code, 302)

    def test_pending_product_as_admin(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get('/product/show/25', {}, format= 'json')
        self.assertEquals(response.status_code, 200)
        self.client.logout()

    def test_report_list(self):
        response = self.client.get('/product/report/list', {}, format= 'json')
        self.assertEquals(response.status_code, 302)

    def test_report_list_as_admin(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get('/product/report/list', {}, format= 'json')
        self.assertEquals(response.status_code, 200)
        self.client.logout()

    def test_product_review(self):
        response = self.client.get('/product/review/26', {}, format= 'json')
        self.assertEquals(response.status_code, 302)

    def test_product_review_as_admin(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get('/product/review/26', {}, format= 'json')
        self.assertEquals(response.status_code, 200)
        self.client.logout()

    def test_product_report(self):
        data = urlencode({
            "reportButton":"Enviar",
            "causa":1,
            "comentarios":"comentario de ejemplo",
        })
        
        response = self.client.post('/product/show/24', data, content_type= 'application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/product/show/24")

    def test_product_comment(self):
        data = urlencode({
            "commentButton":"Enviar",
            "titulo":"Comentario de prueba",
            "mensaje":"Comentario de ejemplo",
        })
        
        response = self.client.post('/product/show/24', data, content_type= 'application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/product/show/24")

    def test_product_add_ubication_supermarket(self):
        data = urlencode({
            "ubicaciones":3,
            "precio":12,
            "addingUbication":"Guardar+ubicación",
        })
        
        response = self.client.post('/product/show/24', data, content_type= 'application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/product/show/24")

    def test_product_add_ubication(self):
        data = urlencode({
            "supermercado":"no",
            "lat":40.403085626411965,
            "lon":-3.707690280456543,
            "nombreComercio":"Comercio nuevo",
            "precio":3,
            "addingUbication":"Guardar+ubicación",
        })
        
        response = self.client.post('/product/show/24', data, content_type= 'application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/product/show/24")

    def test_product_review_accept(self):
        self.client.login(username="admin", password="admin")

        data = urlencode({
            "foto":None,
            "nombre":"Galleta maría sin gluten",
            "descripcion":"Galletas maría sin gluten",
            "precio":2.45,
            "dieta":"Gluten",
            "dieta":"Vegano",
            "dieta":"Vegetariano",
            "dieta":"Marisco",
            "dieta":"Lactosa",
            "dieta":"Frutos secos",
            "ubicaciones":3,
            "revision":"Aceptar",
        })
        
        response = self.client.post('/product/review/26', data, content_type= 'application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/product/show/26")
        self.client.logout()

    def test_product_review_decline(self):
        self.client.login(username="admin", password="admin")

        data = urlencode({
            "foto":None,
            "nombre":"Crunchy Crumbs",
            "descripcion":"Crunchy Crumb: rebozado crujiente sin gluten",
            "precio":1.75,
            "dieta":"Gluten",
            "ubicaciones":3,
            "revision":"Denegar",
        })
        
        response = self.client.post('/product/review/25', data, content_type= 'application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/product/list")
        self.client.logout()

    def test_product_rate(self):
        data = urlencode({
            "id":24,
            "rate":3,
        })
        
        response = self.client.post('/product/show/24/rate', data, content_type= 'application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["success"], "true")
        self.assertEqual(json.loads(response.content)["msj"], "Su voto ha sido procesado")

    def test_product_rate_duplicated(self):
        data = urlencode({
            "id":24,
            "rate":3,
        })
        self.client.post('/product/show/24/rate', data, content_type= 'application/x-www-form-urlencoded')
        response = self.client.post('/product/show/24/rate', data, content_type= 'application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["success"], "false")
        self.assertEqual(json.loads(response.content)["msj"], "Ya ha realizado una valoración")

    def test_report_accept(self):
        self.client.login(username="admin", password="admin")

        data = urlencode({
            "reportButton":"Enviar",
            "causa":1,
            "comentarios":"comentario de ejemplo",
        })
        self.client.post('/product/show/24', data, content_type= 'application/x-www-form-urlencoded')

        data = urlencode({
            "revision":"Resuelto",
        })
        response = self.client.post('/product/report/action/1', data, content_type= 'application/x-www-form-urlencoded')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/product/report/list")
        self.client.logout()

    def test_report_decline(self):
        self.client.login(username="admin", password="admin")

        data = urlencode({
            "reportButton":"Enviar",
            "causa":1,
            "comentarios":"comentario de ejemplo",
        })
        self.client.post('/product/show/24', data, content_type= 'application/x-www-form-urlencoded')

        data = urlencode({
            "revision":"No Procede",
        })
        response = self.client.post('/product/report/action/1', data, content_type= 'application/x-www-form-urlencoded')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/product/report/list")
        self.client.logout()

    def test_product_create(self):

        with open("static/img/logo.png", 'rb') as f:
            foto = SimpleUploadedFile("logo.png", f.read(),content_type="image/png")

            data = {
                    "nombre":"Sopa do macaco",
                    "descripcion":"Sopa de cacao sin gluten",
                    "precio":2.12,
                    "dieta":"Gluten",
                    "ubicaciones":2,
                    "foto":foto,
                }

            response = self.client.post('/product/create', data, format= 'multipart')

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, "/product/list")

    def test_product_create_no_name(self):

        with open("static/img/logo.png", 'rb') as f:
            foto = SimpleUploadedFile("logo.png", f.read(),content_type="image/png")

            data = {
                    "descripcion":"Sopa de cacao sin gluten",
                    "precio":2.12,
                    "dieta":"Gluten",
                    "ubicaciones":2,
                    "foto":foto,
                }

            response = self.client.post('/product/create', data, format= 'multipart')
            self.assertEqual(response.status_code, 200)
