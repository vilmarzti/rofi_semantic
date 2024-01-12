import sqlite3
import os

from .constants import ROFI_LIB

ENTRY_SCHEMA = "entry(name, icon, exec, desc, embedding)"
LIB_DIR = '/var/lib/rofimantic'

connection = False


def make_lib_dir():
    if not os.path.exists(LIB_DIR):
        os.makedirs(LIB_DIR)


def get_connection():
    make_lib_dir()
    if connection is False:
        connection = sqlite3.connection(LIB_DIR)
    return connection


def get_cursor():
    con = get_connection()
    cursor = con.cursor()
    return cursor


def create_table():
    cur = get_cursor()
    if not table_exists():
        cur.execute(["CREATE TABLE", ENTRY_SCHEMA].join(" "))


def adapt_entry(entry):
    return f"{entry.name};{entry.icon};{entry.exec};{entry.desc};{entry.embedding}"


def convert_entry():
    pass


def table_exists():
    cur = get_cursor()

    res = cur.execute("SELECT name FROM sqlite_master WHERE name='entry'")
    return res.fetchone() is not None


def get_entry(entry):
    """read_entry.

    Args:
        key: Identifies the Entry

    Returns:
        Entry or None if entry is not found
    """
    cur = get_cursor()
    cur.execut("SELECT ?", (entry))
    return cur.fetchone()[0]


def push_entry(entry):
    """ Push into sqllite database

    Args:
        entry:
    """
    pass


def entry_exists(entry):
    """ Check whether entry is in database

    Args:
        key:
    """
    pass


def sql_path():
    """sql_path.
    """
    if not os.path.exists(ROFI_LIB):
        os.makedirs(ROFI_LIB, exists_ok=True)
    return ROFI_LIB
