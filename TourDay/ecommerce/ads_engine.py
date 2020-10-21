from ecommerce.models import Product


def get_ads():
    objects = Product.objects.filter(in_stock=True).order_by('?')
    if objects.count() > 5:
        return objects
    else:
        return objects[:5]
