# coding=utf-8
from decimal import Decimal

from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4, A5
from reportlab.lib.units import cm
from django.http import HttpResponse
import os

from core_settings.settings import INV_CURRENCY

try:
    from django.utils import importlib
except ImportError:
    import importlib

from core_settings import settings


def format_currency(amount, tax=None):
    if tax:
        amount -= amount * Decimal(tax/100)
    return "{} {:.2f} {}".format(
        settings.INV_CURRENCY_SYMBOL, amount, ""
    )


def pdf_response(draw_funk, file_name, *args, **kwargs):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=\"%s\"" % file_name
    draw_funk(response, *args, **kwargs)
    return response


def draw_header(canvas):
    """ Draws the invoice header """
    canvas.setStrokeColorRGB(0.9, 0.5, 0.2)
    canvas.setFillColorRGB(0.2, 0.2, 0.2)
    canvas.setFont('Helvetica', 16)
    canvas.drawString(18 * cm, -1 * cm, 'Invoice')
    canvas.drawInlineImage(settings.INV_LOGO, 1 * cm, -1 * cm, 25, 25)  # LOGO SIZE : 25x25
    canvas.setLineWidth(4)
    canvas.line(0, -1.25 * cm, 21.7 * cm, -1.25 * cm)


def draw_address(canvas):
    """ Draws the business address """
    business_details = (
        settings.COMPANY_TITLE,
        u'STREET',
        u'TOWN',
        U'COUNTY',
        U'POSTCODE',
        U'COUNTRY',
        u'',
        u'',
        u'Phone: +00 (0) 000 000 000',
        u'Email: example@example.com',
        u'Website: www.example.com',
        u'Reg No: 00000000'
    )
    canvas.setFont('Helvetica', 9)
    textobject = canvas.beginText(13 * cm, -2.5 * cm)
    for line in business_details:
        textobject.textLine(line)
    canvas.drawText(textobject)


def draw_footer(canvas):
    """ Draws the invoice footer """
    note = (
        u'Bank Details: {}, '.format(settings.COMPANY_TITLE),
        u'Sort Code: 00-00-00 Account No: 00000000 (Quote invoice number).',
        u'Please pay via bank transfer or cheque. All payments should be made in {}.'.format(settings.INV_CURRENCY),
        u'Make cheques payable to {}.'.format(settings.COMPANY_TITLE),
    )
    textobject = canvas.beginText(1 * cm, -27 * cm)
    for line in note:
        textobject.textLine(line)
    canvas.drawText(textobject)


class Address(object):
    contact_name = "Person"
    address_one = "socity"
    address_two = "sec-16"
    town = "Gandhinagar"
    country = "India"
    postcode = "382021"


class Invoice(object):
    address = Address()
    invoice_id = "123"
    invoice_date = "12 June 2018"
    currency = "INR"
    items = []
    # address = "Gandhinagar"

    def total(self):
        return 556


def draw_pdf(buffer, invoice):
    """ Draws the invoice """
    canvas = Canvas(buffer, pagesize=A4)
    canvas.translate(0, 29.7 * cm)
    canvas.setFont('Helvetica', 10)

    canvas.saveState()
    draw_header(canvas)
    canvas.restoreState()

    canvas.saveState()
    draw_footer(canvas)
    canvas.restoreState()

    canvas.saveState()
    draw_address(canvas)
    canvas.restoreState()

    # Client address
    textobject = canvas.beginText(1.5 * cm, -2.5 * cm)
    contact_name = invoice.customer.name
    contact_number = invoice.customer.contact_number.as_international
    if contact_name:
        textobject.textLine(contact_name)
    if invoice.customer.address:
        if invoice.customer.address.address_one:
            textobject.textLine(invoice.customer.address.address_one)
        if invoice.customer.address.address_two:
            textobject.textLine(invoice.customer.address.address_two)
        if invoice.customer.address.city:
            textobject.textLine(invoice.customer.address.city.name)
        # if invoice.customer.address.state:
        #     textobject.textLine(invoice.address.state.name)
        if invoice.customer.address.zip_code:
            textobject.textLine(invoice.customer.address.zip_code)
        if invoice.customer.address.country:
            textobject.textLine(invoice.customer.address.country.name)
    if contact_number:
        textobject.textLine(contact_number)
    canvas.drawText(textobject)

    # Info
    textobject = canvas.beginText(1.5 * cm, -6.75 * cm)
    textobject.textLine(u'Invoice ID: %s' % invoice.invoice_id)
    textobject.textLine(u'Invoice Date: %s' % invoice.printable_sale_date)
    textobject.textLine(u'Client: %s' % invoice.customer.name)
    canvas.drawText(textobject)

    # Items
    data = [[u'Quantity', u'Description', "Tax", "Amount", u'Total'], ]
    for item in invoice.items.all():
        data.append([
            item.quantity,
            item.cost.name,
            "{} %".format(item.cost.tax),
            format_currency(item.cost.price.amount, tax=item.cost.tax),
            format_currency(item.cost.price.amount)
        ])
    data.append([u'', u'', '', u'Total:', str(invoice.get_total)])
    table = Table(data, colWidths=[2 * cm, 9 * cm, 2 * cm, 3 * cm, 3 * cm])
    table.setStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
        ('GRID', (0, 0), (-1, -2), 1, (0.7, 0.7, 0.7)),
        ('GRID', (-2, -1), (-1, -1), 1, (0.7, 0.7, 0.7)),
        ('ALIGN', (-2, 0), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
    ])
    tw, th, = table.wrapOn(canvas, 15 * cm, 19 * cm)
    table.drawOn(canvas, 1 * cm, -8 * cm - th)

    canvas.showPage()
    canvas.save()


if __name__ == "__main__":
    location = os.path.join(settings.BASE_DIR, "invoice.pdf")
    draw_pdf(location, Invoice())
