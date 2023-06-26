
from tienda.models import *
from django.forms import ModelForm

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'direccion']

