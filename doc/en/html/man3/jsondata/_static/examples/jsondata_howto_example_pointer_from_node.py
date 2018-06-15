# -*- coding:utf-8   -*-
from __future__ import absolute_import
from __future__ import print_function

from jsondata.jsondata import JSONData
from jsondata.jsonpointer import JSONPointer

# JSON document
jdata = { 'a': { 'b': { 'c': 2, 'd': 3 } } }

targetnode = jdata['a']['b']['c']
jsondata = JSONData(jdata)

path_list = fetch_pointerpath(targetnode, jdata)
path = JSONPointer(path_list[0])

print()
print('["' + str(path) + '"] = ' + str(path_list))
print()
