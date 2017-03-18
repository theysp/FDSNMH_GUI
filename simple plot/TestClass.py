# -*- coding: utf-8 -*-

import copy
class NumberList:
    def __init__(self):
        self.numbers=[]

    def add_number(self,num):
        self.numbers.append(num)

    def __mul__(self,othernum):
        new_num_list = copy.deepcopy(self)
        for i in range(len(new_num_list.numbers)):
            new_num_list.numbers[i] *= othernum
        return new_num_list

if __name__ == '__main__':
    numlist = NumberList()
    numlist.add_number(1)
    numlist.add_number(2)
    numlist.add_number(3)
    newlist = numlist * 4
    print(newlist.numbers)