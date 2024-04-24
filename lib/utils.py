import os
from PIL import Image
from django.conf import settings


def attach_logo(main_image):
    logo_image = Image.open(os.path.join(settings.BASE_DIR, "lib/logo.png"))
    logo_width, logo_height = logo_image.size
    main_width, main_height = main_image.size
    min_dim = min(main_width, main_height)
    left = (main_width - min_dim) // 2
    top = (main_height - min_dim) // 2
    right = (main_width + min_dim) // 2
    bottom = (main_height + min_dim) // 2
    main_image = main_image.crop((left, top, right, bottom))
    main_image = main_image.resize((800, 800), )
    main_width, main_height = main_image.size
    min_dim = min(main_width, main_height)
    max_logo_size = min_dim // 4
    if logo_width > max_logo_size or logo_height > max_logo_size:
        logo_image.thumbnail((max_logo_size, max_logo_size))
    logo_position = (min_dim - logo_image.width - 20, 20)
    main_image.paste(logo_image, logo_position, logo_image)
    return main_image


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
