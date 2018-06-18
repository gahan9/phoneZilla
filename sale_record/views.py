import os

from django.http import HttpResponse, HttpResponseBadRequest, FileResponse
from django.shortcuts import render

from django.views.generic.base import View
from reportlab.pdfgen import canvas

from core_settings.settings import INV_ROOT
from main.utils import draw_pdf
from sale_record.models import *

__author__ = "Gahan Saraiya"


class InvoiceGenerateView(View):
    def get(self, request, **kwargs):
        print("Generating invoice..")
        pk = self.kwargs.get("pk")
        try:
            sale_invoice = SaleRecord.objects.get(pk=pk)
            print("Found invoice id: {}".format(sale_invoice.invoice_id))
            file_name = "{}_{}.pdf".format(sale_invoice.invoice_id, sale_invoice.printable_sale_date)
            file_location = os.path.join(INV_ROOT, file_name)
            draw_pdf(file_location, sale_invoice)
            return FileResponse(open(file_location, "rb"), content_type="application/pdf")
        except SaleRecord.DoesNotExist as e:
            err_msg = str(e)
            response = "No invoice exist for given query"
            return HttpResponse(response)
