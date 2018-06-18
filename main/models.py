# coding=utf-8
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField

from core_settings.settings import PRODUCT_TYPE

__author__ = "Gahan Saraiya"

__all__ = ['BaseDistributor', 'BaseEffectiveCost', 'BaseProductRecord', 'BasePurchaseRecord', 'BaseCustomer', 'BaseSaleRecord',
           'BaseAddress', 'BaseCity', 'BaseState', 'BaseCountry']


class BaseState(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class BaseCity(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class BaseCountry(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class BaseAddress(models.Model):
    contact_name = models.CharField(max_length=255, null=True, blank=True,
                                    verbose_name=_("Contact Person Name"))
    address_one = models.TextField(blank=True, null=True,
                                   verbose_name=_("Address Line 1"))
    address_two = models.TextField(blank=True, null=True,
                                   verbose_name=_("Address Line 2"))
    zip_code = models.CharField(max_length=6, blank=True, null=True,
                                verbose_name=_("Postal Code"))

    @property
    def printable_address(self):
        address = ""
        address += "{}\n".format(self.contact_name) if self.contact_name else ""
        address += "{}\n".format(self.address_one) if self.address_one else ""
        address += "{}\n".format(self.address_two) if self.address_two else ""
        return address

    def __str__(self):
        return self.printable_address[:20] + "..." if len(self.printable_address) > 20 else self.printable_address

    class Meta:
        abstract = True


class BaseDistributor(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name=_("Company Name"),
                            help_text=_("Enter Name of the company from which you are making your purchase"))
    contact_number = PhoneNumberField(blank=True, null=True,
                                      verbose_name=_("Contact Number"),
                                      help_text=_("Enter Phone Number with country code: i.e. +919988776655"))
    alternate_contact_number = PhoneNumberField(blank=True, null=True,
                                                verbose_name=_("Alternate Contact Number"),
                                                help_text=_("Enter Phone Number with country code: i.e. +919988776655"))
    fax_number = models.IntegerField(blank=True, null=True,
                                     verbose_name=_("Fax Number"))
    address = models.TextField(_("Postal Address"), blank=True, null=True,
                               help_text=_("Address of distributor"))
    email_address = models.EmailField(blank=True, null=True,
                                      verbose_name=_("Email Address"),
                                      help_text=_("i.e. example@domain.com"))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def has_fax_number(self):
        return bool(self.fax_number)

    @property
    def has_email(self):
        return bool(self.email_address)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Supplier detail"
        verbose_name_plural = "Supplier Details"
        abstract = True


class BaseProductRecord(models.Model):
    CATEGORIES = (
        (5, 5),
        (12, 12),
        (18, 18),
        (28, 28),
    )
    COLLECTION = (
        (1, '(CGST/SGST)'),
        (2, '(IGST)'),
    )
    name = models.CharField(max_length=255,
                            verbose_name=_(PRODUCT_TYPE + " Name"),
                            help_text=_("Enter Name/Title of Item"))
    price = MoneyField(decimal_places=2, max_digits=11,
                       default=0, default_currency='INR',
                       verbose_name=_("MRP of " + PRODUCT_TYPE))
    available_stock = models.IntegerField(blank=True, null=True,
                                          default=0, validators=[MinValueValidator(0)])
    product_image = models.ImageField(upload_to='media/uploads/', blank=True, null=True)
    hsn_code = models.CharField(max_length=8, blank=True, null=True)
    tax = models.IntegerField(blank=True, null=True,
                              default=5,
                              choices=CATEGORIES,
                              verbose_name=_("Tax"))
    tax_type = models.IntegerField(blank=True, null=True,
                                   default=1, choices=COLLECTION,
                                   verbose_name=_("Tax Type"),
                                   help_text=_("Tax collection type"))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def split_name(self, size=20):
        name = [self.name[i:i+size] for i in range(0, len(self.name), size)]
        return '\n'.join(name)

    @property
    def has_image(self):
        return bool(self.product_image)

    @property
    def get_image(self):
        if self.has_image:
            return self.product_image.url
        else:
            return None

    def __str__(self):
        return "{} @ {}".format(self.name, self.price)

    class Meta:
        abstract = True
        verbose_name = verbose_name_plural = PRODUCT_TYPE + " Detail"


class BaseEffectiveCost(models.Model):
    discount = models.IntegerField(default=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(blank=True, null=True,
                                   default=1,
                                   validators=[MinValueValidator(1)],
                                   verbose_name=_("Qty."))

    @property
    def details(self):
        return self.__dict__

    class Meta:
        abstract = True
        verbose_name = verbose_name_plural = "Effective cost of " + PRODUCT_TYPE


class BasePurchaseRecord(models.Model):
    PAYMENT_MODE = (
        (1, _("Cash")),
        (2, _("Cheque")),
        (3, _("Card")),
        (4, _("Online Transfer NEFT/RTGS")),
        (5, _("Credit/EMI/Loan")),
    )
    invoice_id = models.CharField(max_length=80, blank=True, null=True,
                                  verbose_name=_("Enter Invoice Number"),
                                  help_text=_("Enter Order/Invoice Number"))
    purchase_date = models.DateField(default=timezone.now,
                                     help_text=_("Enter date of purchase/invoice"))
    delivery_date = models.DateField(blank=True, null=True,
                                     help_text=_("Date of order received"))
    total_amount = MoneyField(
        decimal_places=2, default=0,
        blank=True, null=True,
        default_currency='INR', max_digits=11,
        verbose_name=_("Total Invoice Amount"),
        help_text=_("Total Payable Invoice Amount [Discounted Rate]"))
    payment_mode = models.IntegerField(choices=PAYMENT_MODE)
    payment_status = models.BooleanField(
        default=False,
        verbose_name=_("Payment Status (in transit/dispute)"),
        help_text=_("mark if payment isn't processed immediately"))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def is_paid(self):
        # to test a case - if payment mode is specified then paid status needs to be true
        return bool(self.payment_mode)

    def __str__(self):
        return self.invoice_id

    class Meta:
        abstract = True
        verbose_name = "Purchase Details of " + PRODUCT_TYPE
        verbose_name_plural = "Purchase Details of item from various suppliers"


class BaseCustomer(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name=_("Customer Name"),
                            help_text=_("Enter Name of the customer who is purchasing"))
    contact_number = PhoneNumberField(blank=True, null=True,
                                      verbose_name=_("Contact Number"),
                                      help_text=_("Enter Phone Number with country code: i.e. +919988776655"))
    alternate_contact_number = PhoneNumberField(blank=True, null=True,
                                                verbose_name=_("Alternate Contact Number"),
                                                help_text=_("Enter Phone Number with country code: i.e. +919988776655"))
    address = models.TextField(_("Postal Address"), blank=True, null=True,
                               help_text=_("Address of distributor"))
    email_address = models.EmailField(blank=True, null=True,
                                      verbose_name=_("Email Address"),
                                      help_text=_("i.e. example@domain.com"))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def has_email(self):
        return bool(self.email_address)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = "Customer detail"
        verbose_name_plural = "Customer Details"


class BaseSaleRecord(models.Model):
    PAYMENT_MODE = (
        (1, _("Cash")),
        (2, _("Cheque")),
        (3, _("Card")),
        (4, _("Online Transfer NEFT/RTGS")),
        (5, _("Credit/EMI/Loan")),
    )
    invoice_id = models.CharField(max_length=80, blank=True, null=True,
                                  verbose_name=_("Enter Invoice Number"),
                                  help_text=_("Enter Order/Invoice Number"))
    sale_date = models.DateField(blank=True, null=True,
                                 default=timezone.now,
                                 verbose_name=_("Sale Date"),
                                 help_text=_("Enter date of purchase/invoice"))
    delivery_date = models.DateField(blank=True, null=True,
                                     help_text=_("Date of order delivered"))
    payment_mode = models.IntegerField(choices=PAYMENT_MODE, blank=True, null=True)
    cancelled = models.BooleanField(
        default=False,
        verbose_name=_("Cancelled/Refunded"),
        help_text=_("mark if bill cancelled"))
    payment_status = models.BooleanField(
        default=False,
        verbose_name=_("Payment Status (in transit/dispute)"),
        help_text=_("mark if payment isn't processed immediately"))
    payment_date = models.DateField(blank=True, null=True,
                                    default=timezone.now,
                                    verbose_name=_("Payment Date"),
                                    help_text=_("Date of full payment"))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def is_paid(self):
        # to test a case - if payment mode is specified then paid status needs to be true
        return bool(self.payment_mode)

    def __str__(self):
        return self.invoice_id

    class Meta:
        abstract = True
        verbose_name = "Sale record"
        verbose_name_plural = "Sale Records"
