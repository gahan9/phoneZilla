# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from main.models import *
from core_settings.settings import PRODUCT_TYPE, PRODUCT_MAKER


class Distributor(BaseDistributor):
    address2 = models.TextField(_("Postal Address 2"), blank=True, null=True,
                                help_text=_("Alternate/branch Address of distributor"))


class ProductRecord(BaseProductRecord):
    launched_by = models.CharField(max_length=300, blank=True, null=True,
                                   verbose_name=_(PRODUCT_MAKER[PRODUCT_TYPE][0] + " Name"))
    product_launch_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("Date of " + PRODUCT_MAKER[PRODUCT_TYPE][1]))
    version = models.IntegerField(
        blank=True, null=True,
        verbose_name="Edition",
        help_text="Enter Version or Edition of Item (if applicable)")


class EffectiveCost(BaseEffectiveCost):
    """
    This model is only to preserve effective cost of item
    """
    discount = models.IntegerField(default=15)
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


class PurchaseRecord(BasePurchaseRecord):
    items = models.ManyToManyField(EffectiveCost, blank=True)
    purchased_from = models.ForeignKey(
        Distributor, on_delete=models.CASCADE,
        verbose_name=_("Supplier Name"),
        help_text=_("Choose Company from where purchase is made"))

    @property
    def get_total(self):
        try:
            return sum([product.get_total_effective_cost for product in self.items.all()])
        except Exception as e:
            print("Exception in calculating total amount... : " + str(e))
            return '0'

    @property
    def get_items(self):
        return ' | \n'.join([p.get_detail for p in self.items.all()])

