from django.db import models

from billing.models import BillingProfile


class Address(models.Model):
    ADDRESS_TYPE = (
        ('billing', 'Billing'),
        ('shipping', 'Shipping'),
    )
    billing_profile = models.ForeignKey(BillingProfile)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPE)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    zip_code = models.CharField(max_length=120)
    country = models.CharField(max_length=120, default='Polska')

    def __str__(self):
        return "{billing}, {type}".format(billing=self.billing_profile, type=self.address_type)

    def get_address(self):
        return '{line1}\n{line2}\n{city} {zip_code}\n{country}'.format(
            line1=self.address_line_1,
            line2=self.address_line_2 or "",
            city=self.city,
            zip_code=self.zip_code,
            country=self.country
        )
