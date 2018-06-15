# coding=utf-8
from easy_select2.utils import select2_modelform
from nested_inline.admin import NestedModelAdmin
from django.contrib import admin
# from import_export import resources

from main.admin import *
from core_settings.settings import COMPANY_TITLE
from .models import *
from .admin_inlines import *

__author__ = "Gahan Saraiya"

DistributorForm = select2_modelform(Distributor, {'width': "600px"})
ProductRecordForm = select2_modelform(ProductRecord, {'width': "600px"})
PurchaseRecordForm = select2_modelform(PurchaseRecord, {'width': "600px"})
EffectiveCostForm = select2_modelform(EffectiveCost, {'width': "300px"})


class DistributorAdmin(NestedModelAdmin):
    form = DistributorForm
    inlines = [PurchaseRecordInline]
    search_fields = ["name", "address"]
    list_display = ["id", "name", "contact_number", "alternate_contact_number", "fax_number",
                    "address",
                    ]


class ProductRecordAdmin(NestedModelAdmin):
    form = ProductRecordForm
    inlines = [EffectiveCostInline]
    search_fields = ["name", "launched_by"]
    list_display = ["id", "name", "price", "product_launch_date", "launched_by",
                    "version",
                    ]


class EffectiveCostAdmin(BaseEffectiveCostAdmin):
    form = EffectiveCostForm
    search_fields = ["discount"]
    list_display = ["id", "cost", "discount",
                    "get_effective_cost", "get_total_effective_cost"]
    readonly_fields = ["get_effective_cost", "get_total_effective_cost"]


class PurchaseRecordAdmin(BasePurchaseRecordAdmin):
    form = PurchaseRecordForm
    list_display = ["id", "invoice_id", "purchased_from", "purchase_date", "get_items",
                    "get_total", "payment_mode", "payment_status"
                    ]
    readonly_fields = ['get_total']
    fieldsets = (
        (None, {'fields': ["invoice_id"]}),
        ("Items", {'fields': ["items"]}),
        ("Payment Details", {'fields': ["get_total", "payment_mode", "payment_status"]}),
        ("Other Details", {'fields': ["purchased_from", "purchase_date"]}),
    )
    add_fieldsets = (
        (None, {'fields': ["invoice_id"]}),
        ("Items", {'fields': ["items"]}),
        ("Payment Details", {'fields': ["get_total", "payment_mode", "payment_status"]}),
        ("Other Details", {'fields': ["purchased_from", "purchase_date"]}),
    )


# class PurchaseResource(resources.ModelResource):
#     class Meta:
#         model = PurchaseRecord


admin.site.register(Distributor, DistributorAdmin)
admin.site.register(EffectiveCost, EffectiveCostAdmin)
admin.site.register(ProductRecord, ProductRecordAdmin)
admin.site.register(PurchaseRecord, PurchaseRecordAdmin)

admin.site.site_header = COMPANY_TITLE + ' administration'
admin.site.site_title = COMPANY_TITLE + ' administration'
admin.site.index_title = COMPANY_TITLE + ' administration'
