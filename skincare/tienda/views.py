from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from tienda.pay import Carrito
from tienda.models import Producto, Cliente
from tienda.forms import ProductoForm, ClienteForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors 
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle


def index(request):
    return render(request,'index.html')
    
def tienda(request):
    p = Producto.objects.all()
    return render(request, "tienda.html", {'productos':p})

def pagar_Productos(request):
    p1 = Producto.objects.all()
    return render(request,'pagarProductos.html', {'productos':p1})


def RopaAdm(request):
    p = Producto.objects.all()
    return render(request,'ropa.html', {'productos':p})

def agregarP(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return RopaAdm(request)
    else:
        form = ProductoForm()
    return render(request, 'AgregarRopa.html', {'form': form})

def actualizarP(request, idp):
    p1 = Producto.objects.get(id=idp)
    if request.method == 'GET':
        form = ProductoForm(instance=p1)
        return render(request, 'actualizarProducto.html', {'form':form})
    elif request.method == 'POST':
        form = ProductoForm(request.POST, instance=p1)
        if form.is_valid():
            form.save()
        return RopaAdm(request)

def agregarCliente (request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return generar_pdf(request)
    else:
        form = ClienteForm()
    return render(request, 'Cliente.html', {'form': form})

def deleteP(request, idp):
    try:
       r1 = Producto.objects.get(id=idp)
       r1.delete()
       return RopaAdm(request)
    except:
       print('')
       return RopaAdm(request)

def agregarCarrito(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=id)
    c1 = Producto.objects.get(id=id)
    c1.existencia= c1.existencia - 1
    c1.save()
    carrito.agregar(producto)
    return redirect("tienda")


def eliminarCarrito(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=id)
    carrito.eliminar2(producto)
    c1 = Producto.objects.get(id=id)
    c1.existencia= c1.existencia + 1
    c1.save()
    return redirect("pagarProductos")


def pagar_productos(request):
    p1 = Producto.objects.all()
    if not p1:
        carrito = Carrito(request)
        total = 0
        if request.session.carrito.items:
            for key, value in request.session.carrito.items():
                total += value['precio']
            return render(request, 'pagar_productos.html', {'total': total})
        return HttpResponse("No hay productos disponibles.")
    
    return render(request, 'pagarProductos.html', {'productos': p1})


def generar_pdf(request):
    cliente = Cliente.objects.filter(nombre=request.user.username).first()
    if not cliente:
        return HttpResponse('ERROR')

    carrito = request.session["carrito"]
    productos = [[value['nombre'], value['precio'], value['cantidad']] for value in carrito.values()]
    total = sum(value['acumulado'] for value in carrito.values())

    buffer = BytesIO()
    styles = getSampleStyleSheet()
    style_heading = styles['Heading1']
    style_heading.alignment = 1
    style_table = ParagraphStyle(
    name='TableStyle',
    parent=styles['BodyText'],
    fontSize=12,
    fontName='Helvetica-Bold',
    textColor=colors.black,
    alignment=1,
    spaceAfter=12,
    )
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    elements.append(Paragraph('Recibo', style_heading))

# Tabla de productos

    table_data = [['Nombre', 'Precio', 'Cantidad']] + productos
    table = Table(table_data, colWidths=[200, 100, 100])
    table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

# Total
    elements.append(Paragraph(f'Total: ${total}', styles['BodyText']))

    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Compras.pdf"'

# Copiar el contenido del objeto BytesIO al objeto HttpResponse
    response.write(buffer.getvalue())
    return response
