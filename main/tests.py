from django.test import TestCase
from django.contrib.auth.models import User
from product.models import CausaReporte, Ubicacion, Producto, UbicacionProducto
from authentication.models import Perfil, Dieta

def create_ubicacion(nombre):
    ubicacion = Ubicacion(nombre=nombre, latitud=37.3826, longitud=-5.99629)
    ubicacion.save()
    return ubicacion

class BaseTestCase(TestCase):

    def setUp(self):
        #Dietas
        nombres = ["Vegano","Vegetariano","Sin gluten","Sin lactosa","Sin marisco","Sin frutos secos"]
        for nombre in nombres:
            dieta = Dieta(nombre=nombre)
            dieta.save()
        #CausaReportes
        causaReporte1 = CausaReporte(causa="Dietas/restricciones incorrectas")
        causaReporte1.save()
        causaReporte2 = CausaReporte(causa="Producto repetido")
        causaReporte2.save()
        #Usuarios y perfiles
        user_1 = User(username='Usuario1', first_name='usuario1_firstname', last_name='usuario1_lastname')
        user_1.set_password('qwerty')
        user_1.save()
        user_admin = User(username='admin', is_staff=True, is_superuser=True, first_name='admin_firstname', last_name='admin_lastname')
        user_admin.set_password('qwerty')
        user_admin.save()
        perfil_1 = Perfil(user=user_1)
        perfil_1.save()
        perfil_1.dietas.add(Dieta.objects.get(nombre="Vegetariano"))
        perfil_admin = Perfil(user=user_admin)
        perfil_admin.save()
        perfil_admin.dietas.add(Dieta.objects.get(nombre="Sin frutos secos"))
        #Ubicaciones
        ub1 = create_ubicacion("La Veganeria de Triana")
        ub2 = create_ubicacion("La Vegana Sevilla")
        ub3 = create_ubicacion("Panceliac")
        ub4 = Ubicacion(nombre="Dia")
        ub4.save()
        #Productos (3 aceptados y 1 pendiente)
        prod1 = Producto(titulo="Pan pueblo sin gluten ecologico - 400 gr - Zealia",descripcion="Delicioso pan sin gluten de agricultura ecologico que además es apto para intolerantes a la lactosa y alérgicos a la plv y al huevo. Sin grasas hidrogenadas ni trans, sin OMG, sin colorantes ni conservantes.",
        foto="../pan_pueblo.png",precioMedio=2.41,user=perfil_1,estado="Aceptado")
        prod1.save()
        prod1.dietas.add(Dieta.objects.get(nombre="Sin gluten"))
        prod2 = Producto(titulo="Leche desnatada sin lactosa ",descripcion="Seis bricks de leche desnatada sin lactosa.",
        foto="../leche.png",precioMedio=5.09,user=perfil_1,estado="Aceptado")
        prod2.save()
        prod2.dietas.add(Dieta.objects.get(nombre="Vegetariano"))
        prod2.dietas.add(Dieta.objects.get(nombre="Vegano"))
        prod2.dietas.add(Dieta.objects.get(nombre="Sin lactosa"))
        prod3 = Producto(titulo="SPECIAL LINE",descripcion="Bio rollo de hamburguesa vegetal con tofu y algas ecologico envase 750 g",
        foto="../hamburguesa_vegetal.png",precioMedio=3.13,user=perfil_1,estado="Aceptado")
        prod3.save()
        prod3.dietas.add(Dieta.objects.get(nombre="Vegano"))
        prod3.dietas.add(Dieta.objects.get(nombre="Vegetariano"))
        prod4 = Producto(titulo="Pizza Prosciutto & Funghi",descripcion="Pizza de Jamón y Champiñones sin gluten.",
        foto="../pizza.png",precioMedio=4.15,user=perfil_1,estado="Pendiente")
        prod4.save()
        prod4.dietas.add(Dieta.objects.get(nombre="Sin gluten"))
        #UbicacionProducto
        ubicacionProducto1 = UbicacionProducto(producto=prod1, ubicacion=ub1, user=perfil_1, precio = 2.41)
        ubicacionProducto1.save()
        ubicacionProducto2 = UbicacionProducto(producto=prod2, ubicacion=ub3, user=perfil_1, precio = 5.09)
        ubicacionProducto2.save()
        ubicacionProducto3 = UbicacionProducto(producto=prod3, ubicacion=ub2, user=perfil_1, precio = 3.14)
        ubicacionProducto3.save()
        ubicacionProducto4 = UbicacionProducto(producto=prod3, ubicacion=ub4, user=perfil_1, precio = 3.12)
        ubicacionProducto4.save()
        ubicacionProducto5 = UbicacionProducto(producto=prod4, ubicacion=ub1, user=perfil_1, precio = 4.15)
        ubicacionProducto5.save()

    def tearDown(self):
        super().tearDown()