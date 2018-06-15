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


class GTPLlogin(LiveServerTestCase):
    def setUp(self):
        self.login_url = "http://www.gtpl.net/login/login.php"
        self.register_ticket_url = "http://www.gtpl.net/login/register_ticket.php"
        self.my_tickets_url = "http://www.gtpl.net/login/my_tickets.php"
        _path = os.path.join(getattr(settings, 'MEDIA_ROOT'), "credentials.pickle")
        self.credentials = pickler(1, path=_path)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # settings.DEBUG = True
        if sys.platform == "win32":
            cls.selenium = webdriver.Chrome(
                getattr(settings, "CHROME_DRIVER_PATH",
                        r"F:\dev\_selenium\ChromeDriver\chromedriver.exe"))
        else:
            cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(15)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def _test_login(self):
        self.selenium.get(self.login_url)
        self.take_snapshot()
        username_input = self.selenium.find_element_by_name("txtuname")
        username_input.send_keys(self.credentials['username'])  # Enter username
        password_input = self.selenium.find_element_by_name("txtpwd")
        password_input.send_keys(self.credentials['password'])  # Enter password
        self.selenium.execute_script("$('#radio1').click()")  # Select Broadband
        self.selenium.find_element_by_name('submit').click()  # login
        _sleep(5)  # sleep.. (awaits seconds before closing browser)

    def _test_register_ticket(self):
        self.selenium.get(self.register_ticket_url)
        Select(self.selenium.find_element_by_id('category')).select_by_value('TECH_ONL')
        Select(self.selenium.find_element_by_id('subcategory')).select_by_value('BBONL06')
        self.selenium.find_element_by_name('submit').click()
        _sleep(5)
        self.take_snapshot()
        self.scroll()
        _sleep(5)
        self.take_snapshot()

    def _test_display_my_tickets(self):
        self.selenium.get(self.my_tickets_url)
        # self.selenium.maximize_window()
        _sleep(5)
        self.take_snapshot()

    def scroll(self):
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = self.selenium.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.selenium.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def take_snapshot(self):
        _name = "screen-shot_{}.png".format(timezone.now().strftime('%Y-%d-%m_%H.%M.%S'))
        _path = os.path.join(getattr(settings, 'MEDIA_ROOT'), 'selenium', _name)
        self.selenium.save_screenshot(_path)
        _body = self.selenium.find_element_by_tag_name('body')
        # snapshot = _body.screenshot_as_base64
        # snapshot = _body.screenshot_as_png
        # _body.screenshot('snap.png')
        # with open(_path, 'wb') as f:
        #     f.write(snapshot)
        print("Snapshot saved at: {}".format(_path))

    def test_ordered(self):
        # self.selenium.set_window_size('1920', '1080')
        self.selenium.fullscreen_window()
        self._test_login()
        self.take_snapshot()
        _sleep(5)
        self._test_display_my_tickets()
        self._test_register_ticket()
