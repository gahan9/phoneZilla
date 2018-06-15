# coding=utf-8
__author__ = "Gahan Saraiya"
from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class MainConfig(AppConfig):
    name = 'main'


class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'
