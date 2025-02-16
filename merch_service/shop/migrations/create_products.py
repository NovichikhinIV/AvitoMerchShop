from django.db import migrations


def create_products(apps, schema_editor):
    Product = apps.get_model("shop", "Product")
    products = [
        ("t-shirt", 80),
        ("cup", 20),
        ("book", 50),
        ("pen", 10),
        ("powerbank", 200),
        ("hoody", 300),
        ("umbrella", 200),
        ("socks", 10),
        ("wallet", 50),
        ("pink-hoody", 500),
    ]

    for name, price in products:
        Product.objects.get_or_create(name=name, defaults={"price": price})


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0001_initial"),  # последняя миграцию
    ]

    operations = [
        migrations.RunPython(create_products),
    ]
