# -*- coding:utf-8   -*-
from __future__ import absolute_import
from __future__ import print_function

from jsondata.jsondata import JSONData
from jsondata.jsonpointer import JSONPointer

# JSON in-memory document
D = JSONData(
        { 'a': { 'b': { 'c': 2, 'd': 3 } } }
    )
  

# the same as native Pyhton data
rdata = { 'a': { 'b': { 'c': 2, 'd': 3 } } }

# print structure
print(D)
print(repr(D))

