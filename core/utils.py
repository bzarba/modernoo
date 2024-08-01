from django.utils.text import slugify

def generate_unique_slug(instance, slug_field_name='slug'):
    slug = slugify(instance.name)
    model_class = instance.__class__
    unique_slug = slug
    num = 1
    while model_class.objects.filter(**{slug_field_name: unique_slug}).exists():
        unique_slug = f"{slug}-{num}"
        num += 1
    return unique_slug
