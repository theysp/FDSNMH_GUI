# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from base.base import BasicPath
from data_handling.material import *

if __name__ == "__main__":
    with open(BasicPath.element_list_file_name) as input_elemnt:
        lines = [a for a in input_elemnt.readlines() if len(a) > 0]
        elemlist = []
        for line in lines:
            elemlist.append(line.strip('\r\n '))
        for element_name in elemlist:
            print("loading: "+element_name)
            element = ElementPool.get_elem(element_name)
        #element = ElementPool.get_elem("Alloy625")