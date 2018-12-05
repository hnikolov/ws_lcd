#!/usr/bin/python
import time

class LOG(object):
    def __init__(self, prnt = True):
        self.prnt = prnt

    def log(self, data):
        st = time.strftime('%d-%b-%Y %H:%M:%S')
        line = st + ":" + str(data) + '\n'
        if self.prnt == True: print line

        file_name = "log/" + time.strftime('%d-%b-%Y') + "_log.txt"
        with open(file_name, "a+") as fp:
            fp.write(line)
