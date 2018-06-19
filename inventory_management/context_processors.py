# coding=utf-8
__author__ = "Gahan Saraiya"
from core_settings import settings


def site_details(request):
    return {
        "SITE_NAME": settings.COMPANY_TITLE,
        "SITE_LOGO": settings.COMPANY_LOGO,
        "COMPANY_EMAIL": settings.COMPANY_EMAIL,
        "COMPANY_CONTACT_NUMBER": settings.COMPANY_CONTACT_NUMBER,
        "COMPANY_ADDRESS_LINE_ONE": settings.COMPANY_ADDRESS_LINE_ONE,
        "COMPANY_ADDRESS_LINE_TWO": settings.COMPANY_ADDRESS_LINE_TWO,
        "COMPANY_COUNTRY": settings.COMPANY_COUNTRY,
        "COMPANY_WEBSITE": settings.COMPANY_WEBSITE,
        "INV_CURRENCY_SYMBOL": settings.INV_CURRENCY_SYMBOL,
        "INV_CURRENCY_PREFIX": settings.INV_CURRENCY_PREFIX,
        "PRODUCT_TYPE": settings.PRODUCT_TYPE,
        "COPYRIGHT_SINCE": settings.COPYRIGHT_SINCE
    }
