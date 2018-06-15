# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djmoney.models.fields import MoneyField

from main.models import *
from core_settings.settings import PRODUCT_TYPE
from inventory_management.models import ProductRecord

__all__ = ["CustomerDetail", "SaleRecord", "SaleEffectiveCost"]


def increment_invoice_number():
    last_invoice = SaleRecord.objects.all().order_by('id').last()
    if not last_invoice:
        return 1000
    invoice_no = last_invoice.invoice_id
    invoice_int = int(invoice_no)
    new_invoice_int = invoice_int + 1
    new_invoice_no = str(new_invoice_int)
    return new_invoice_no


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
        return "{} :{} @{}%= {}; {} per item {} for total item".format(
            self.cost.name, self.cost.price, self.discount,
            self.get_effective_cost, self.quantity, self.get_total_effective_cost)

    def clean(self):
        self.cost.available_stock = self.cost.available_stock + self.quantity

    def __str__(self):
        return "{} - {}% @ {}".format(self.cost.name, self.discount, self.cost.price)

    class Meta:
        verbose_name = verbose_name_plural = "Effective cost of " + PRODUCT_TYPE


class CustomerDetail(BaseCustomer):
    pass


class SaleRecord(BaseSaleRecord):
    invoice_id = models.CharField(max_length=500, default=increment_invoice_number, null=True, blank=True,
                                  verbose_name=_("Enter Invoice Number"),
                                  help_text=_("Enter Order/Invoice Number"))
    items = models.ManyToManyField(SaleEffectiveCost, blank=True)
    amount = MoneyField(
        decimal_places=2, default=0,
        blank=True, null=True,
        default_currency='INR', max_digits=11,
        verbose_name=_("Total Invoice Amount (considered in case of no book entries added)"),
        help_text=_("Total Payable Invoice Amount [Discounted Rate]*\n*for migration purpose only"))
    customer = models.ForeignKey(CustomerDetail, null=True, blank=True, on_delete=models.CASCADE)

    @property
    def get_total(self):
        try:
            return sum([product.get_total_effective_cost for product in self.items.all()])
        except Exception as e:
            print("Exception in calculating total amount... : " + str(e))
            return self.amount

    @property
    def get_items(self):
        return ' | \n'.join([p.get_detail for p in self.items.all()])
