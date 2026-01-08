# coding=utf-8
from rest_framework import serializers

from .models import PurchaseRecord, ProductRecord, EffectiveCost, Distributor
from main.serializers import BaseDistributorSerializer



class PurchaseRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PurchaseRecord
        fields = ["id", "url", "invoice_id", "purchase_date",
                  "purchased_from", "purchase_date", "delivery_date",
                  "items", "payment_mode", "payment_status",
                  "total_amount"]
        # fields = "__all__"


class ProductRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductRecord
        fields = "__all__"


class EffectiveCostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EffectiveCost
        fields = "__all__"


class DistributorSerializer(BaseDistributorSerializer):
    class Meta:
        model = Distributor
        fields = BaseDistributorSerializer.Meta.fields + ['address2']
