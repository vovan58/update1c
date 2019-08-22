#!/bin/python
# -*- coding: UTF-8 -*-

import logging
import configparser
import os
import sys
import argparse
import re
import shutil
from select import select

class gvk_message:

    def __init__(self,log_name):
        self.verbose = False
        self.silence = False
        self.level = logging.INFO
        self.dict_level = {'NOTSET':logging.NOTSET,'DEBUG':logging.DEBUG, 'INFO':logging.INFO,
                      'WARNING':logging.WARNING, 'ERROR':logging.ERROR, 'CRITICAL':logging.CRITICAL}
        self.prog_name = ''
        self.max_level = logging.NOTSET
        self.log_name = log_name
        self.file_name ='service1c.log'
        self.full_file_name =''
        self.path = ''
        self.clean = False
        if os.name == 'nt':
            self.path = os.path.join(os.getenv('APPDATA'),'1C')
        elif os.name == 'posix':
            self.path = os.path.join('~','.1C')
        self.logger = logging.getLogger(log_name)

    def set_params(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--log", action='store_true', default=False) # выводить в журнал
        parser.add_argument("--log_level", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO')
        parser.add_argument("--log_path")
        parser.add_argument("--log_name")
        parser.add_argument("--log_clean", action='store_true', default=False)
        parser.add_argument("--verbose", action='store_true', default=True)
        parser.add_argument('--silence', action='store_true', default=False) # без вывода в stdout, stderr

        namespace = parser.parse_args(sys.argv[1:])
        level        = namespace.log_level
        self.silence = namespace.silence
        self.verbose = namespace.verbose
        self.clean   = namespace.log_clean
        path = namespace.log_path
        if path != None:
            if os.path.exists(path):
                if os.path.isdir(path):
                    self.path = path
        else:
            path = ''
        name = namespace.log_name
        if name != None:
            self.file_name = name
        self.full_file_name = self.file_name
        if (path != ""):
            if os.path.isdir(path):
                self.full_file_name = os.path.join(self.path, self.file_name)
            else:
                self.full_file_name = self.file_name
                print("Not log dir. Log dir is current dir")
        log_mode = "a"
        if (self.clean):
            log_mode = "w"
        fh = logging.FileHandler(self.full_file_name, log_mode, encoding="UTF-8")
        formatter = logging.Formatter(u'%(asctime)s %(levelname)-8s [%(name)s] %(message)s')
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.level = self.dict_level.get(level)
        if self.level == None:
            self.level = logging.INFO
            self.logger.warning('Error log level "' + level + '". Set log level "INFO"')
        self.logger = logging.getLogger(self.log_name)

    def first_message(self,prog_name):
        self.prog_name  = prog_name
        self.put_std_out(logging.INFO,'begin work')

    def last_message(self):
        max_level_str = ''
        for key,items in self.dict_level.items():
            if items == self.max_level:
                max_level_str = key
                break
        self.put_std_out(logging.INFO,'end work. Max level message : ' + str(max_level_str))

    def notset(self,message):
        self.put_std_out(logging.NOTSET, message)

    def debug(self,message):
        if logging.DEBUG > self.max_level:
            self.max_level = logging.DEBUG
        self.put_std_out(logging.DEBUG, message)

    def info(self,message):
        if logging.INFO > self.max_level:
            self.max_level = logging.INFO
        self.put_std_out(logging.INFO, message)

    def warning(self,message):
        if logging.WARNING > self.max_level:
            self.max_level = logging.WARNING
        self.put_std_out(logging.WARNING, message)

    def error(self,message):
        if logging.ERROR > self.max_level:
            self.max_level = logging.ERROR
        self.put_std_out(logging.ERROR, message)

    def critical(self,message):
        if logging.CRITICAL > self.max_level:
            self.max_level = logging.CRITICAL
        self.put_std_out(logging.CRITICAL, message)

    def put_std_out(self,level,message):
        msg = '['+self.prog_name+'] ' + message
        self.logger.log(level,msg)
        if not self.silence:
            if self.verbose or level >= logging.INFO :
                print (message)
