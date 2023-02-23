from django.db import models

class Product(models.Model):
    DATA_PRODUCTS = [
        ('sc', 'stream chemistry'),
        ('sd', 'stream discharge'),
        ('pc', 'precipitation chemistry'),
        ('pv', 'precipitation volume'),
    ]

    prod_id = models.BigAutoField(primary_key=True)
    prod_select = models.BooleanField()
    prod_name = models.CharField(max_length=50,
                                choices = DATA_PRODUCTS)
    def prod_status(self):
        return self.prod_select

    def __str__(self):
        return self.prod_name

