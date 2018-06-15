# -*- coding:utf-8   -*-
from __future__ import absolute_import
from __future__ import print_function

from jsondata.jsondata import JSONData
from jsondata.jsonpointer import JSONPointer

# JSON document
D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})

target = JSONPointer('/a/b')

sourcenode = {'alternate': 4711 }

D.branch_replace(target, 'f', sourcenode)

print(D)
#print(repr(D))