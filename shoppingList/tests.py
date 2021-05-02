from shoppingList.models import ListaDeCompra
from authentication.models import Perfil, User
from main.tests import BaseTestCase
from product.models import Producto

def create_list():
    lista_compra = ListaDeCompra(perfil=Perfil.objects.get(user =User.objects.get(username="Usuario1")))
    lista_compra.save()
    lista_compra.productos.add(Producto.objects.get(titulo="SPECIAL LINE"))
    return lista_compra
class RecetaTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_create_list(self):
        create_list()
        list_compra = ListaDeCompra.objects.get(perfil=Perfil.objects.get(user =User.objects.get(username="Usuario1")))
        self.assertEqual(list_compra.productos.count(),1)

    def test_update_list(self):
        list_compra = create_list()
        list_compra.productos.add(Producto.objects.get(titulo="Leche desnatada sin lactosa "))
        self.assertEqual(list_compra.productos.count(),2)

    def test_delete_list(self):
        list_compra = create_list()
        list_pk = list_compra.pk
        self.assertEqual(ListaDeCompra.objects.filter(pk=list_pk).count(), 1)
        list_compra.delete()
        self.assertEqual(ListaDeCompra.objects.filter(pk=list_pk).count(), 0)