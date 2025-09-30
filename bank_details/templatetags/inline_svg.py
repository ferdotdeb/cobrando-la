# bank_details/templatetags/inline_svg.py
from django import template
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def inline_svg(path: str) -> str:
    """
    Inserta el contenido de un archivo SVG estático inline en la plantilla.
    Uso: {% inline_svg 'brands/visa.svg' %}
    """
    full = finders.find(path)
    if not full:
        return ""  # opcional: muestra placeholder
    try:
        with open(full, "r", encoding="utf-8") as f:
            return mark_safe(f.read())
    except Exception:
        return ""
