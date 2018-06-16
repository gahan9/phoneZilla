# coding=utf-8
__author__ = "Gahan Saraiya"
import os
import time

import sys
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, LiveServerTestCase
from django.urls import reverse_lazy
from django.utils import timezone
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from inventory_management.utils import pickler


def _sleep(seconds=2, flag=True):
    if flag:
        time.sleep(seconds)


class PurchaseTest(TestCase):
    pass


class LoginTestSelenium(StaticLiveServerTestCase):
    def setUp(self):
        self.credentials = {
            "username": "root",
            "password": "r@123456"
        }
        User.objects.create(username=self.credentials['username'],
                            password=make_password(self.credentials['password']))

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # settings.DEBUG = True
        # driver = webdriver.Chrome(r"F:\dev\_selenium\ChromeDriver\chromedriver.exe")
        cls.selenium = webdriver.Chrome(getattr(settings, "CHROME_DRIVER_PATH", r"F:\dev\_selenium\ChromeDriver\chromedriver.exe"))
        cls.selenium.implicitly_wait(15)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('{}{}'.format(self.live_server_url, reverse_lazy('login')))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(self.credentials['username'])
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(self.credentials['password'])
        self.selenium.find_element_by_id('login').click()
        time.sleep(5)
