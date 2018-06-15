# coding=utf-8
__author__ = "Gahan Saraiya"
from core_settings.settings import COMPANY_TITLE, COMPANY_LOGO, PRODUCT_TYPE, COPYRIGHT_SINCE


def site_details(request):
    return {
        "SITE_NAME": COMPANY_TITLE,
        "PRODUCT_TYPE": PRODUCT_TYPE,
        "SITE_LOGO": COMPANY_LOGO,
        "COPYRIGHT_SINCE": COPYRIGHT_SINCE
    }
