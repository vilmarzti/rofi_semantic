import sqlite3
import os

from .constants import ROFI_LIB


def create_table():
    pass


def sql_path():
    if not os.path.exists(ROFI_LIB):
        os.makedirs(ROFI_LIB, exists_ok=True)
    return ROFI_LIB

