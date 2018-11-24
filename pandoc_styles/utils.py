'''Some utility functions'''

import logging
import subprocess
from os import chdir, getcwd
from os.path import join, isfile, normpath
from contextlib import contextmanager
from .constants import CONFIG_DIR, USER_DIR_PREFIX, PATH_MISC


def file_read(file_name, *path, encoding="utf-8"):
    '''Just a wrapper, since nearly always only read or write are used in this script'''
    if path:
        path = path + (file_name,)
        file_name = join(path[0], *path[1:])
    with open(file_name, encoding=encoding) as ffile:
        return ffile.read()


def file_write(file_name, string, *path, mode="w", encoding="utf-8"):
    '''Just a wrapper, since nearly always only read or write are used in this script'''
    if path:
        path = path + (file_name,)
        file_name = join(path[0], *path[1:])
    with open(file_name, mode, encoding=encoding) as ffile:
        ffile.write(string)
    return file_name


def run_process(name, args=""):
    """Run a process with the given args and return True if successfull """
    try:
        subprocess.run(f"{name} {args}", check=True)
        return True
    except subprocess.CalledProcessError:
        logging.error(f"{name} failed!")
        logging.debug(f"{name} command-line:\n{name} {args}!")
        return False
    except FileNotFoundError:
        logging.error(f'{name} not found!')
        return False


def has_extension(ffile, extensions):
    '''Check if ffile has an extension given in extensions. Extensions can be
    a string or a list of strings.'''
    if ffile.rpartition('.')[-1] in make_list(extensions):
        return True
    return False


def make_list(item):
    """Make a list with item as its member, if item isn't a list already"""
    if not isinstance(item, list):
        return [item]
    return item


@contextmanager
def change_dir(new_dir):
    """Changes to the given directory, returns to the current one after"""
    current_dir = getcwd()
    chdir(new_dir)
    yield
    chdir(current_dir)

def expand_directories(item, key=""):
    """
    Look if item is a file in the configuration directory and return the path if
    it is. Searches first for the given path, then looks into a subfolder given by
    key and finally in the "misc" subfolder. If no file is found, just return item.
    """
    if isinstance(item, str) and USER_DIR_PREFIX in item:
        for folder in ["", key, PATH_MISC]:
            test_file = normpath(item.replace("~", join(CONFIG_DIR, folder)))
            if isfile(test_file):
                return test_file.replace("\\", "/")
    return item
