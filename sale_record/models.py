# coding=utf-8
import os

from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from djmoney.models.fields import MoneyField

from main.models import *
from core_settings.settings import PRODUCT_TYPE
from inventory_management.models import ProductRecord

__all__ = ["CustomerDetail", "SaleRecord", "SaleEffectiveCost", "PathMapping", "Address", "City", "State", "Country"]

__author__ = "Gahan Saraiya"


class City(BaseCity):
    pass


class State(BaseState):
    pass


class Country(BaseCountry):
    pass


class Address(BaseAddress):
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.PROTECT)
    state = models.ForeignKey(State, blank=True, null=True, on_delete=models.PROTECT)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.PROTECT)

    @property
    def printable_address(self):
        address = ""
        address += "{}\n".format(self.contact_name) if self.contact_name else ""
        address += "{}\n".format(self.address_one) if self.address_one else ""
        address += "{}\n".format(self.address_two) if self.address_two else ""
        address += "{},".format(self.city.name) if self.city else ""
        address += "{}".format(self.state.name) if self.state else ""
        address += "-{}\n".format(self.zip_code) if self.zip_code else ""
        address += "{}".format(self.country) if self.country else ""
        return address

    def __str__(self):
        return self.printable_address[:20] + "..." if len(self.printable_address) > 20 else self.printable_address


def increment_invoice_number():
    last_invoice = SaleRecord.objects.all().order_by('id').last()
    if not last_invoice:
        return 1000
    invoice_no = last_invoice.invoice_id
    invoice_int = int(invoice_no)
    new_invoice_int = invoice_int + 1
    new_invoice_no = str(new_invoice_int)
    return new_invoice_no


class PathMapping(models.Model):
    TYPE = (
        (1, "Invoice Storage"),
        (2, "Other")
    )
    invoice_path = models.TextField()
    category = models.IntegerField(choices=TYPE, default=1)

    class Meta:
        verbose_name = "Store Default path"


class SaleEffectiveCost(BaseEffectiveCost):
    """
    This model is only to preserve effective cost of item
    """
    discount = models.IntegerField(default=0)
    cost = models.ForeignKey(ProductRecord, on_delete=models.CASCADE)

    @property
    def get_effective_cost(self):
        return (self.cost.price.amount * (100 - self.discount)) / 100 if self.discount else self.cost.price.amount

    @property
    def get_total_effective_cost(self):
        return self.get_effective_cost * self.quantity

    @property
    def get_detail(self):
        return "{} >> [Disc. {}%] [MRP: {}] [Qty. {}] [item cost: {}] [total bill: {}]".format(
            self.cost.name,  self.discount, self.cost.price, self.quantity,
            self.get_effective_cost, self.get_total_effective_cost)

    def clean(self):
        self.cost.available_stock = self.cost.available_stock + self.quantity

    def __str__(self):
        return "{} >> [Disc. {}%] [MRP: {}] [Qty. {}]".format(self.cost.name, self.discount, self.cost.price, self.quantity)

    class Meta:
        verbose_name = verbose_name_plural = "Effective cost of " + PRODUCT_TYPE


class CustomerDetail(BaseCustomer):
    address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.PROTECT,
                                verbose_name=_("Postal Address"),
                                help_text=_("Address"))


class SaleRecord(BaseSaleRecord):
    invoice_id = models.CharField(max_length=500, default=increment_invoice_number, null=True, blank=True,
                                  verbose_name=_("Enter Invoice Number"),
                                  help_text=_("Enter Order/Invoice Number"))
    items = models.ManyToManyField(SaleEffectiveCost, blank=True)
    customer = models.ForeignKey(CustomerDetail, null=True, blank=True, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.PROTECT,
                                verbose_name=_("Postal Address"),
                                help_text=_("Address"))

    @property
    def get_total(self):
        return sum([product.get_total_effective_cost for product in self.items.all()])

    @property
    def get_items(self):
        return ' | \n'.join([p.get_detail for p in self.items.all()])

    @property
    def printable_sale_date(self):
        return self.sale_date.strftime("%d %b %Y")

    def get_reference_id(self):
        _id = self.id
        _url = reverse_lazy('generate_invoice', kwargs={"pk": _id})
        _href = "<a href='{0}'>print</a>".format(_url)
        return format_html(_href)


@receiver(m2m_changed, sender=SaleRecord.items.through, dispatch_uid="update_stock_count")
def update_stock(sender, instance, action, **kwargs):
    if action is "post_add":
        for item in instance.items.all():
            item.cost.available_stock -= item.quantity
            item.cost.save()
