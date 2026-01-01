from django import template
from django.conf import settings
import cloudinary

register = template.Library()

@register.filter
def cloudinary_url(image_field):
    if image_field:
        if hasattr(image_field, 'url'):
            return image_field.url
        return image_field
    return None
