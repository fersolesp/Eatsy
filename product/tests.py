from product.models import Ubicacion, UbicacionProducto, Producto, CausaReporte, Reporte, Valoracion, Aportacion
from authentication.models import Perfil, Dieta
from django.contrib.auth.models import User
from main.tests import BaseTestCase

def create_ubicacion():
    ubicacion = Ubicacion(nombre="Red Verde", latitud=37.41063, longitud=-5.99099)
    ubicacion.save()
    return ubicacion

def create_ubicacion_sup():
    ubicacion = Ubicacion(nombre="Mercadona", latitud=0.000000, longitud=0.000000)
    ubicacion.save()
    return ubicacion

def create_product():
    ub1 = create_ubicacion()
    ub2 = create_ubicacion_sup()
    user = Perfil.objects.get(user =User.objects.get(username="Usuario1"))
    producto = Producto(titulo="Tofu",descripcion="Es una buena fuente de proteínas de calidad, calcio y minerales.",
    precioMedio=10,user=user)
    producto.save()
    producto.dietas.add(Dieta.objects.get(nombre="Vegetariano"))
    producto.dietas.add(Dieta.objects.get(nombre="Vegano"))
    producto.dietas.add(Dieta.objects.get(nombre="Sin lactosa"))
    ubicacionProducto1 = UbicacionProducto(producto=producto, ubicacion=ub1, user=user, precio = 9)
    ubicacionProducto1.save()
    ubicacionProducto2 = UbicacionProducto(producto=producto, ubicacion=ub2, user=user, precio = 11)
    ubicacionProducto2.save()
    return producto

def create_report():
    producto = create_product()
    user = User.objects.get(username="Usuario1")
    causa = CausaReporte.objects.get(causa="Producto repetido")
    estado = "Pendiente"
    reporte = Reporte(producto=producto, user=user, causa=str(causa), comentarios = "Este producto está repetido",estado=estado)
    reporte.save()
    return reporte

def create_valoracion():
    producto = create_product()
    user = Perfil.objects.get(user =User.objects.get(username="Usuario1"))
    puntuacion = 4
    valoracion = Valoracion(producto=producto, puntuacion=puntuacion, user=user)
    valoracion.save()
    return valoracion

def create_aportacion():
    producto = create_product()
    user = Perfil.objects.get(user =User.objects.get(username="Usuario1"))
    titulo = "Producto insustituible"
    mensaje = "Un producto insustituible para vegetarianos, e interesante para todos."
    aportacion = Aportacion(producto=producto, titulo=titulo, mensaje=mensaje, user=user)
    aportacion.save()
    return aportacion

class UbicacionTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_create_ubicacion(self):
        create_ubicacion()
        ub_sup=create_ubicacion_sup()
        ub = Ubicacion.objects.get(nombre="Red Verde")
        self.assertEqual(float(ub.latitud),37.41063)
        self.assertEqual(float(ub.longitud),-5.99099)
        self.assertFalse(ub.esSupermercado)
        self.assertTrue(str(ub_sup),"Mercadona")
        self.assertTrue(ub_sup.esSupermercado)

    def test_update_ubicacion(self):
        ub = create_ubicacion()
        ub.nombre = "Redes Verdes"
        ub.latitud = 37.4210
        ub.save()
        ubicacion = Ubicacion.objects.get(pk=ub.pk)
        self.assertEqual(float(ub.latitud),37.4210)
        self.assertEqual(str(ubicacion),"Redes Verdes")

    def test_delete_ubicacion(self):
        ub = create_ubicacion()
        ub_pk = ub.pk
        self.assertEqual(Ubicacion.objects.filter(pk=ub_pk).count(), 1)
        ub.delete()
        self.assertEqual(Ubicacion.objects.filter(pk=ub_pk).count(), 0)

class ProductoTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_create_product(self):
        create_product()
        prod = Producto.objects.get(titulo="Tofu")
        self.assertEqual(prod.estado,"Pendiente")
        self.assertEqual(prod.user.user.username,"Usuario1")
        self.assertEqual(prod.dietas.count(),3)
        dietas = [dieta.nombre for dieta in prod.dietas.all()]
        self.assertIn("Vegetariano",dietas)
        self.assertIn("Vegano",dietas)
        self.assertIn("Sin lactosa",dietas)
        ubicaciones = UbicacionProducto.objects.filter(producto=prod)
        self.assertIn("Mercadona",str(ubicaciones))

    def test_update_product(self):
        prod = create_product()
        prod.titulo = "Queso de soja"
        prod.estado = "Aceptado"
        prod.save()
        producto = Producto.objects.get(pk=prod.pk)
        self.assertEqual(producto.estado,"Aceptado")
        self.assertEqual(str(producto),"Queso de soja")

    def test_delete_product(self):
        prod = create_product()
        prod_pk = prod.pk
        self.assertEqual(Producto.objects.filter(pk=prod_pk).count(), 1)
        prod.delete()
        self.assertEqual(Producto.objects.filter(pk=prod_pk).count(), 0)

class ReporteTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_create_report(self):
        create_report()
        prod = Producto.objects.get(titulo="Tofu")
        reporte = Reporte.objects.get(producto=prod)
        self.assertEqual(str(reporte),"Tofu (Producto repetido)")

    def test_update_report(self):
        rep = create_report()
        rep.estado = "No procede"
        rep.save()
        reporte = Reporte.objects.get(pk=rep.pk)
        self.assertEqual(reporte.estado,"No procede")

    def test_delete_report(self):
        reporte = create_report()
        reporte_pk = reporte.pk
        self.assertEqual(Reporte.objects.filter(pk=reporte_pk).count(), 1)
        reporte.delete()
        self.assertEqual(Reporte.objects.filter(pk=reporte_pk).count(), 0)

class ValoracionTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_create_valoracion(self):
        create_valoracion()
        prod = Producto.objects.get(titulo="Tofu")
        valoracion = Valoracion.objects.get(producto=prod)
        self.assertEqual(str(valoracion),"Tofu: 4")

    def test_update_valoracion(self):
        val = create_valoracion()
        val.puntuacion = 5
        val.save()
        valoracion = Valoracion.objects.get(pk=val.pk)
        self.assertEqual(valoracion.puntuacion,5)
    
    def test_delete_valoracion(self):
        val = create_valoracion()
        val_pk = val.pk
        self.assertEqual(Valoracion.objects.filter(pk=val_pk).count(), 1)
        val.delete()
        self.assertEqual(Valoracion.objects.filter(pk=val_pk).count(), 0)

class AportacionTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
    
    def test_create_aportacion(self):
        create_aportacion()
        prod = Producto.objects.get(titulo="Tofu")
        aportacion = Aportacion.objects.get(producto=prod)
        self.assertEqual(str(aportacion),"Producto insustituible")
    
    def test_update_aportacion(self):
        aport = create_aportacion()
        aport.mensaje = "Un producto muy bueno para vegetarianos, e interesante para todos."
        aport.save()
        aportacion = Aportacion.objects.get(pk=aport.pk)
        self.assertEqual(aportacion.mensaje,"Un producto muy bueno para vegetarianos, e interesante para todos.")

    def test_delete_aportacion(self):
        aportacion = create_aportacion()
        aportacion_pk = aportacion.pk
        self.assertEqual(Aportacion.objects.filter(pk=aportacion_pk).count(), 1)
        aportacion.delete()
        self.assertEqual(Aportacion.objects.filter(pk=aportacion_pk).count(), 0)
