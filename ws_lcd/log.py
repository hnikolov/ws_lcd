#!/usr/bin/python
import time

class LOG(object):
    """ Levels:
        0 - No logging
        1 - Errors
        2 - Errors and Warnings
        3 - Errors, Warnings, Info
    """
    def __init__(self, prnt = True, level = 1):
        self.prnt  = prnt
        self.level = level # Error, Warning, Info

    def error(self, data):
        if self.level >= 1:
            self.log( data )

    def warning(self, data):
        if self.level >= 2:
            self.log( data )

    def info(self, data):
        if self.level >= 3:
            self.log( data )

    def log(self, data):
        st = time.strftime('%d-%m-%Y %H:%M:%S')
        line = st + ":" + str(data) + '\n'
        if self.prnt == True: print line

        file_name = time.strftime('%d-%m-%Y') + "_log.txt"
        with open(file_name, "a+") as fp:
            fp.write(line)
