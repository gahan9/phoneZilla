# coding=utf-8
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from main.models import BaseDistributor, BaseProductRecord, BaseEffectiveCost, BasePurchaseRecord

from core_settings.settings import PRODUCT_TYPE, PRODUCT_MAKER


class Distributor(BaseDistributor):
    address2 = models.TextField(_("Postal Address 2"), blank=True, null=True,
                                help_text=_("Alternate/branch Address of distributor"))


class ProductRecord(BaseProductRecord):
    launched_by = models.CharField(max_length=300,
                                   verbose_name=_(PRODUCT_MAKER[PRODUCT_TYPE][0] + " Name"))
    product_launch_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("Date of " + PRODUCT_MAKER[PRODUCT_TYPE][1]))
    version = models.IntegerField(
        blank=True, null=True,
        verbose_name=_("Other Model Detail"),
        help_text=_("Other Model Detail"))
    specs = models.TextField(blank=True, null=True,
                             verbose_name=_("Product Specs"),
                             help_text=_("Enter Product specification or any other related details"))
    product_link = models.URLField(blank=True, null=True,
                                   verbose_name=_("Product Link (if any)"))


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
        return "{} >> [Disc. {}%] [MRP: {}] [Qty. {}] [item cost: {}] [total bill: {}]".format(
            self.cost.name,  self.discount, self.cost.price, self.quantity,
            self.get_effective_cost, self.get_total_effective_cost)

    def clean(self):
        self.cost.available_stock = self.cost.available_stock + self.quantity

    def __str__(self):
        return "{} >> [Disc. {}%] [MRP: {}] [Qty. {}]".format(self.cost.name, self.discount, self.cost.price, self.quantity)

    class Meta:
        verbose_name = verbose_name_plural = "Effective cost of " + PRODUCT_TYPE


class PurchaseRecord(BasePurchaseRecord):
    items = models.ManyToManyField(EffectiveCost)  # blank=True not mentioned to enable stock management
    purchased_from = models.ForeignKey(
        Distributor, on_delete=models.CASCADE,
        verbose_name=_("Supplier Name"),
        help_text=_("Choose Company from where purchase is made"))

    @property
    def get_total(self):
        return sum([product.get_total_effective_cost for product in self.items.all()])

    @property
    def get_items(self):
        return ' | \n'.join([p.get_detail for p in self.items.all()])

    def get_bill_amount(self):
        return self.get_total

    def get_bill_items(self):
        return self.get_items

    get_bill_items.short_description = "Items"
    get_bill_amount.short_description = "Bill Amount"


@receiver(m2m_changed, sender=PurchaseRecord.items.through, dispatch_uid="update_stock_count")
def update_stock(sender, instance, action, **kwargs):
    if action == "post_add":
        for item in instance.items.all():
            item.cost.available_stock += item.quantity
            item.cost.save()
