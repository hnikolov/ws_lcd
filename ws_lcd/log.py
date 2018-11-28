#!/usr/bin/python
import time

class LOG(object):
    def __init__(self, prnt = True):
        self.prnt = prnt

    def log(self, data):
        st = time.strftime('%m-%d-%Y %H:%M:%S')
        line = st + ":" + str(data) + '\n'
        if self.prnt == True: print line

        file_name = time.strftime('%Y-%m-%d') + "_log.txt"
        with open(file_name, "a+") as fp:
            fp.write(line)
