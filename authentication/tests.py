from authentication.models import Perfil, Dieta
from django.contrib.auth.models import User
from main.tests import BaseTestCase

def create_perfil(username,dietas):
        user = User(username=username, first_name='usuario_firstname', last_name='usuario_lastname')
        user.set_password('qwerty')
        user.save()
        perfil = Perfil(user=user)
        perfil.save()
        for dieta in dietas:
            perfil.dietas.add(Dieta.objects.get(nombre=dieta))
        return perfil

class PerfilTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_create_perfil(self):
        dietas = ["Vegano","Sin lactosa"]
        perfil = create_perfil("prueba",dietas)
        self.assertEqual(str(perfil),"prueba")
        self.assertEqual(perfil.dietas.count(),2)
        dietas = [str(dieta) for dieta in perfil.dietas.all()]
        self.assertIn("Vegano",dietas)
        self.assertIn("Sin lactosa",dietas)

    def test_update_perfil(self):
        dietas = ["Vegetariano"]
        perfil = create_perfil("prueba",dietas)
        self.assertEqual(perfil.dietas.count(),1)
        perfil.dietas.add(Dieta.objects.get(nombre="Sin frutos secos"))
        self.assertEqual(perfil.dietas.count(),2)

    def test_delete_perfil(self):
        dietas = ["Vegano","Sin frutos secos"]
        perfil = create_perfil("prueba",dietas)
        perfil_pk = perfil.pk
        self.assertEqual(Perfil.objects.filter(pk=perfil_pk).count(), 1)
        perfil.delete()
        self.assertEqual(Perfil.objects.filter(pk=perfil_pk).count(), 0)