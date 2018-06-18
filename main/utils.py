# coding=utf-8
from decimal import Decimal

from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4, A5
from reportlab.lib.units import cm
from django.http import HttpResponse
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from core_settings import settings

# setup unicode fonts
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))


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
    # write company name
    canvas.setFont('Helvetica-Bold', 11)
    textobject = canvas.beginText(13 * cm, -2.5 * cm)
    textobject.textLine(settings.COMPANY_TITLE)
    canvas.drawText(textobject)
    # write GST Reg. No.
    canvas.setFont('Helvetica-Bold', 10)
    textobject = canvas.beginText(13 * cm, -7.5 * cm)
    textobject.textLine('GST Registration No: {}'.format(settings.GST_NUMBER))
    canvas.drawText(textobject)

    # write company details
    business_details = [
        settings.COMPANY_ADDRESS_LINE_ONE,
        settings.COMPANY_ADDRESS_LINE_TWO,
        settings.COMPANY_COUNTRY,
        '',
        '',
        'Phone: {}'.format(settings.COMPANY_CONTACT_NUMBER),
        'Email: {}'.format(settings.COMPANY_EMAIL),
    ]
    if settings.COMPANY_WEBSITE:
        business_details.append('Website: {}'.format(settings.COMPANY_WEBSITE))
    canvas.setFont('Helvetica', 9)
    textobject = canvas.beginText(13 * cm, -3.0 * cm)
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
    data = [['Qty.', 'Item', "Unit\nPrice", "Discount", "Tax\nRate", "Tax\nType", "Tax\nAmount", "Net\nAmount", 'Total\nAmount'], ]
    col_size = [1 * cm, 6.000 * cm, 2.00 * cm, 2.000 * cm, 1.000 * cm, 1.500 * cm, 2.00 * cm, 2.00 * cm, 2.00 * cm]
    for item in invoice.items.all():
        data.append([
            item.quantity,
            item.cost.split_name(6 * 5),
            format_currency(item.product_amount - item.tax_amount),
            "-₹{}".format(item.calculate_discount),
            "{} %".format(item.cost.tax),
            '\n'.join(item.cost.get_tax_type_display().split("/")),
            format_currency(item.tax_amount),
            format_currency(item.get_effective_cost),
            format_currency(item.get_total_effective_cost)
        ])
    data.append(['', '', '', '', '', '', '', 'Total:', format_currency(invoice.get_total)])
    table = Table(data, colWidths=col_size)  # 22 cm total
    table.setStyle([
        # table header style
        ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
        # table content style
        ('FONT', (0, 1), (-1, -1), 'Vera'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
        ('GRID', (0, 0), (-1, -2), 1, (0.7, 0.7, 0.7)),
        ('GRID', (-2, -1), (-1, -1), 1, (0.7, 0.7, 0.7)),
        ('ALIGN', (-2, 0), (-1, -1), 'LEFT'),
    ])
    tw, th, = table.wrapOn(canvas, 15 * cm, 22 * cm)  # 19 cm by default
    table.drawOn(canvas, 0.6 * cm, -8 * cm - th)

    canvas.showPage()
    canvas.save()


if __name__ == "__main__":
    from sale_record.models import SaleRecord
    location = os.path.join(settings.INV_ROOT, "invoice.pdf")
    draw_pdf(location, SaleRecord.objects.last())
