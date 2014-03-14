#!/usr/bin/env python

"""
some test code to demonstrate circular references
"""

import sys
import gc

import mem_check

import circular
reload(circular)

# create a bunch in a loop:
for i in range(50):
    print "iterartion:", i
    p = circular.MyParent()
    p.addChild()
    p.addChild()
    p.addChild()
    print "ref count:", sys.getrefcount(p)
    print "mem_use:", mem_check.get_mem_use()
    del p 
    #gc.collect()
