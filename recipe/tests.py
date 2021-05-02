from recipe.models import Receta
from authentication.models import Perfil, User
from main.tests import BaseTestCase
from product.models import Producto

def create_receta():
    receta = Receta(nombre="Prueba",descripcion="Receta de prueba",perfil=Perfil.objects.get(user =User.objects.get(username="Usuario1")))
    receta.save()
    receta.productos.add(Producto.objects.get(titulo="SPECIAL LINE"))
    return receta
class RecetaTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_create_receta(self):
        create_receta()
        receta = Receta.objects.get(nombre="Prueba")
        self.assertEqual(receta.descripcion,"Receta de prueba")

    def test_update_receta(self):
        rec =  create_receta()
        rec.descripcion = "Receta actualizada"
        rec.save()
        receta = Receta.objects.get(pk=rec.pk)
        self.assertEqual(receta.descripcion,"Receta actualizada")

    def test_delete_receta(self):
        rec = create_receta()
        rec_pk = rec.pk
        self.assertEqual(Receta.objects.filter(pk=rec_pk).count(), 1)
        rec.delete()
        self.assertEqual(Receta.objects.filter(pk=rec_pk).count(), 0)
