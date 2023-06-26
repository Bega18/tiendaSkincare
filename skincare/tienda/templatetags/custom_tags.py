from django import template

register = template.Library()

@register.simple_tag
def sum_values(a, b):
    return a + b

@register.filter
def total(carrito):
    acumulado = 0
    for key, value in carrito.items():
        acumulado += value['acumulado']
    return acumulado