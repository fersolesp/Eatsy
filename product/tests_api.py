from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command

# Create your tests here.

class BaseTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.token = None

    def tearDown(self):
        self.client = None
        self.token = None

    def login(self, user='admin', password='admin'):
        data = {'username': user, 'password': password}
        response = self.client.post('admin/login/?next=/admin/', data, format= 'json')
        self.assertEqual(response.status_code, 200)
        self.token = response.json().get('token')
        self.assertTrue(self.token)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def logout(self):
        self.client.credentials()

class InitialTestCase(BaseTestCase):
    def setUp(self):
        call_command("collectstatic", interactive=False)
        call_command("flush", interactive=False)
        call_command("loaddata", "datosEjemplo.json")
        super().setUp()

    def tearDown(self):
        super().tearDown()
        call_command("flush", interactive=False)

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

