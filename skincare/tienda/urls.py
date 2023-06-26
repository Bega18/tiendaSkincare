from django.urls import path
from . import views
app_name = 'tienda'

urlpatterns = [
    path('', views.index, name ='index'),
    path('tienda/', views.tienda, name ='tienda'),
    path('agregar/', views.agregarP, name ='agregar'),
    path('pagarProductos/', views.pagar_Productos, name ='pagarProductos'),
    path('generar-pdf/', views.generar_pdf, name='generar_pdf'),
    path('actualizar/<int:idp>', views.actualizarP, name ='actualizar'),
    path('delete/<int:idp>', views.deleteP, name="delete"),
    path('agregarCliente/', views.agregarCliente, name ='agregarCliente'),
]