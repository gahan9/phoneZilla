# coding=utf-8
from django.contrib import admin

from nested_inline.admin import NestedModelAdmin

from core_settings.settings import COMPANY_TITLE
from .admin_inlines import EffectiveCostInline, PurchaseRecordInline


__author__ = "Gahan Saraiya"

__all__ = ['BaseDistributorAdmin', 'BaseProductRecordAdmin', 'BaseEffectiveCostAdmin', 'BasePurchaseRecordAdmin', 'BaseCustomerDetailAdmin', 'BaseSaleRecordAdmin']
# PurchaseCompanyForm = select2_modelform(PurchaseCompany, {'width': "600px"})
# BaseProductRecordForm = select2_modelform(BaseProductRecord, {'width': "600px"})
# PurchaseRecordForm = select2_modelform(BaseProductRecord, {'width': "600px"})
# BaseEffectiveCostForm = select2_modelform(BaseEffectiveCost, {'width': "300px"})


class BaseDistributorAdmin(NestedModelAdmin):
    inlines = [PurchaseRecordInline]
    search_fields = ["name", "address"]
    list_display = ["id", "name", "contact_number", "alternate_contact_number", "fax_number", "address"
                    ]


class BaseProductRecordAdmin(NestedModelAdmin):
    inlines = [EffectiveCostInline]
    search_fields = ["name", "launched_by"]
    list_display = ["id", "name", "price", "product_launch_date", "launched_by",
                    "version",
                    ]


class BaseEffectiveCostAdmin(admin.ModelAdmin):
    # form = BaseEffectiveCostForm
    search_fields = ["discount"]
    list_display = ["id", "cost", "discount", "effective_cost", "total_effective_cost"]
    readonly_fields = ["effective_cost", "total_effective_cost"]

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


class BasePurchaseRecordAdmin(admin.ModelAdmin):
    search_fields = ["name", "address"]
    list_display = ["id", "invoice_id", "purchased_from", "purchase_date", "get_items",
                    "total_amount", "payment_mode", "payment_status"
                    ]
    readonly_fields = ["total_amount"]
    fieldsets = (
        (None, {'fields': ["invoice_id"]}),
        ("Items", {'fields': ["items"]}),
        ("Payment Details", {'fields': ["total_amount", "payment_mode", "payment_status"]}),
        ("Other Details", {'fields': ["purchased_from", "purchase_date"]}),
    )
    add_fieldsets = (
        (None, {'fields': ["invoice_id"]}),
        ("Items", {'fields': ["items"]}),
        ("Payment Details", {'fields': ["payment_mode", "payment_status"]}),
        ("Other Details", {'fields': ["purchased_from", "purchase_date"]}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


class BaseCustomerDetailAdmin(admin.ModelAdmin):
    search_fields = ['name', 'contact_number', 'address']
    list_display = ['name', 'contact_number', 'address']
    fieldsets = (
        (None, {'fields': ["name"]}),
        ("Details", {'fields': ["contact_number", "alternate_contact_number", "email_address", "address"]}),
    )
    add_fieldsets = (
        (None, {'fields': ["name"]}),
        ("Details", {'fields': ["contact_number", "alternate_contact_number", "email_address", "address"]}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


class BaseSaleRecordAdmin(admin.ModelAdmin):
    search_fields = ["name", "address"]
    list_display = ["id", "invoice_id", "purchase_date", "get_items",
                    "payment_mode", "payment_status"
                    ]
    fieldsets = (
        (None, {'fields': ["invoice_id"]}),
        ("Items", {'fields': ["items"]}),
        ("Payment Details", {'fields': ["payment_mode", "payment_status"]}),
        ("Other Details", {'fields': ["purchase_date"]}),
    )
    add_fieldsets = (
        (None, {'fields': ["invoice_id"]}),
        ("Items", {'fields': ["items"]}),
        ("Payment Details", {'fields': ["payment_mode", "payment_status"]}),
        ("Other Details", {'fields': ["purchase_date"]}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


admin.site.site_header = COMPANY_TITLE + ' administration'
admin.site.site_title = COMPANY_TITLE + ' administration'
admin.site.index_title = COMPANY_TITLE + ' administration'
