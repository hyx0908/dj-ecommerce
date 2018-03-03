import random
import string
import os

from django.utils.text import slugify


def random_string_generator(size=4, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_key_generator(instance):
    size = random.randint(30, 45)
    key = random_string_generator(size=size)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return key


def unique_order_id_generator(instance):
    new_order_id = random_string_generator(size=10)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=new_order_id).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return new_order_id


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator()
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def get_filename_ext(filepath):
    name, ext = os.path.splitext(filepath)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 654321)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f'products/{new_filename}/{final_filename}'
