"""
URL configuration for skincare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tienda.views import tienda, agregarCarrito, eliminarCarrito, pagar_Productos
from tienda import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tienda/', tienda, name="tienda"),
    path('Pagar/', pagar_Productos, name="pagarProductos"),
    path('agregar/<int:id>/', agregarCarrito, name="agregarCarrito"),
    path('eliminar/<int:id>/', eliminarCarrito, name='eliminarCarrito'),
    path('generar-pdf/', views.generar_pdf, name='generar_pdf'),
    path('',include('tienda.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]