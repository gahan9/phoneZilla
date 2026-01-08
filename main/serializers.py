# coding=utf-8
from rest_framework import serializers

from .models import BasePurchaseRecord, BaseProductRecord, BaseEffectiveCost, BaseDistributor


__author__ = "Gahan Saraiya"

__all__ = ["BaseDistributorSerializer", "BaseEffectiveCostSerializer", "BasePurchaseRecordSerializer", "BaseProductRecordSerializer"]


class BasePurchaseRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BasePurchaseRecord
        fields = ["id", "url", "invoice_id", "purchase_date",
                  "purchased_from", "purchase_date", "delivery_date",
                  "items", "payment_mode", "payment_status",
                  "total_amount"]
        # fields = "__all__"


class BaseProductRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BaseProductRecord
        fields = ["id", "url", "name", "price",
                  "available_stock", "product_image", "date_created",
                  "date_updated"]


class BaseEffectiveCostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BaseEffectiveCost
        fields = "__all__"


class BaseDistributorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BaseDistributor
        fields = ["id", "url", "name", "contact_number", "alternate_contact_number",
                  "fax_number", "address", "email_address", "date_created"]
