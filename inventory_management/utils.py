# coding=utf-8
import os
import pickle

__author__ = "Gahan Saraiya"


def pickler(flag=0, **kwargs):
    file = kwargs.get("path", r"F:\dev\gahantraders\user_files\credentials.pickle")
    credentials = kwargs.get("credentials", {"username": None, "password": None})
    if flag == 0:  # encode
        with open(file, 'wb') as f:
            pickle.dump(credentials, f)
    if flag == 1:  # decode
        with open(file, 'rb') as f:
            credentials = pickle.load(f)
        return credentials
