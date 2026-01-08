# coding=utf-8
__author__ = "Gahan Saraiya"
import os
import time

import sys
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import unittest
from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from .models import ProductRecord



def _sleep(seconds=2, flag=True):
    if flag:
        time.sleep(seconds)


class SimpleModelTest(TestCase):
    def test_product_creation(self):
        from djmoney.money import Money
        product = ProductRecord.objects.create(
            name="Test Phone",
            price=Money(10000, "INR"),
            available_stock=10,
            launched_by="Test Manufacturer"
        )
        self.assertEqual(product.name, "Test Phone")
        self.assertIn("10,000.00", str(product))



@unittest.skipIf(not getattr(settings, "CHROME_DRIVER_PATH", None) or not os.path.exists(getattr(settings, "CHROME_DRIVER_PATH", "")), "Selenium driver not found")
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
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver_path = getattr(settings, "CHROME_DRIVER_PATH", "")
        service = Service(executable_path=driver_path)
        try:
            cls.selenium = webdriver.Chrome(service=service, options=chrome_options)
            cls.selenium.implicitly_wait(15)
        except Exception as e:
            print(f"Failed to start Selenium: {e}")
            raise unittest.SkipTest("Selenium driver failed to start")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'selenium'):
            cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('{}{}'.format(self.live_server_url, reverse('login')))
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys(self.credentials['username'])
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys(self.credentials['password'])
        self.selenium.find_element(By.ID, 'login').click()
        _sleep(2)

