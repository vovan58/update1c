#!/bin/python
# -*- coding: UTF-8 -*-

import logging
import configparser
import os
import sys
import argparse
import re
import shutil
from logging import Logger

def create_config(path=""):
    """
    Create a config file
    """
    if (path == ""):
        filename = "service1c.ini"
    else:
        filename = path
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "path1c", "C:\\Program Files (x86)\\1cv8\\8.3.12.1595\\bin")
    config.set("Settings", "path_rac", "C:\\Program Files (x86)\\1cv8\\8.3.12.1595\\bin")
    config.set("Settings", "path_ras", "C:\\Program Files (x86)\\1cv8\\8.3.12.1595\\bin")
    # config.set("Settings", "font_info",
    #          "You are using %(font)s at %(font_size)s pt")

    with open(filename, "w") as config_file:
        config.write(config_file)

def get_config(path):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        create_config(path)

    config = configparser.ConfigParser()
    config.read(path)
    return config

def get_setting(path, section, setting):
    """
    Print out a setting
    """
    config = get_config(path)
    value = config.get(section, setting)
    msg = "{section} {setting} is {value}".format(
        section=section, setting=setting, value=value
    )

    print(msg)
    return value

def update_setting(path, section, setting, value):
    """
    Update a setting
    """
    config = get_config(path)
    config.set(section, setting, value)
    with open(path, "w") as config_file:
        config.write(config_file)

def delete_setting(path, section, setting):
    """
    Delete a setting
    """
    config = get_config(path)
    config.remove_option(section, setting)
    with open(path, "w") as config_file:
        config.write(config_file)

def set_logger(path="", level='INFO', clean=False):
    """

    :type path: object
    """
    # logging.basicConfig(format = u'[%(asctime)s] %(levelname)-8s %(message)s', level = logging.DEBUG)
    logger = logging.getLogger("gvk_upd")
    map_level = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR,
                 'CRITICAL': logging.CRITICAL}
    log_level = map_level.get(level)
    if (log_level == None):
        log_level = logging.INFO

    logger.setLevel(level)

    name_log = "service1c.log"
    if (path != ""):
        if os.path.isdir(path):
            name_log = os.path.join(path, "service1c.log")
        else:
            print("Not log dir. Log dir is current dir")
    log_mode: str = "a"
    if (clean):
        log_mode = "a+"
    fh = logging.FileHandler("new_snake.log", log_mode, encoding="UTF-8")
    formatter = logging.Formatter(u'%(asctime)s %(levelname)-8s [%(name)s] %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    log_level = map_level.get(level)
    if (log_level == None):
        logger.warning('Error log level "' + level + '". Set log level "INFO"')
    # logger.info(u'начало работы')
    # logger.info(u'конец работы')

def lock_ib_server(server_name, ib_name, lock_code):
    logger = logging.getLogger('gvk_upd')
    logger.info('begin lock ib =' + ib_name + ' server=' + server_name)

def clearcash1c(dir_cash1):
    global logger
    dir_cash = dir_cash1
    pattern = '[0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}'
    for ep in os.listdir(dir_cash):
        if ((re.match(pattern, ep) != None) and os.path.isdir(os.path.join(dir_cash, ep))):
            logger.info('cash directory :' + os.path.join(dir_cash, ep))
            try:
                shutil.rmtree(os.path.join(dir_cash,ep))
                logger.info(os.path.join(dir_cash,ep))
            except Exception as err_x :
                logger.error(os.path.join(dir_cash,ep))
                logger.error(err_x)

def cashclear():
    global logger
    #logger = logging.getLogger('gvk_upd')
    logger.info('begin cash 1c clean')
    pattern = '[0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}'
    if os.name == 'nt': # для Windows начиная с версии Vista
        clearcash1c(os.path.join(os.environ['LOCALAPPDATA'],'1C','1cv8'))
        clearcash1c(os.path.join(os.environ['APPDATA'],'1C','1cv8'))

def main():
    """
    --log_clean
    --log_level=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    :return:
    """
    global logger
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=['init', 'backup', 'restore', 'lock', 'unlock', 'cashclear'])
    parser.add_argument("--log_level", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO')
    parser.add_argument("--log_clean", action='store_true', default=False)
    parser.add_argument("--server") # <сервер:порт/информационнаябаза>
    parser.add_argument('--file')   # полный путь к директории с инфобазой для файлового варианта
    parser.add_argument('--lock_code', default='VXOD')

    namespace = parser.parse_args(sys.argv[1:])
    set_logger(level=namespace.log_level, clean=namespace.log_clean)
    logger = logging.getLogger('gvk_upd')
    logger.info('Begin of work')

    action = namespace.action
    logger.info(sys.argv)
    logger.info(action)
    if (action == "init"):
        create_config()
    elif (action == "backup"):
        lock_ib_server(namespace.server_name, namespace.ib_name, namespace.lock_code)
        pass
    elif (action == "restore"):
        pass
    elif (action == "lock"):
        pass
    elif (action == "unlock"):
        pass
    elif (action == "cashclear"):
        cashclear()
        pass
    else:
        message = "Not action set"
        print(message)
        logger.error(message)

    logger.info('End of work')

# if __name__ == '__main__' :
main()
