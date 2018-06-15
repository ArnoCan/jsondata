# -*- coding:utf-8   -*-
from __future__ import absolute_import
from __future__ import print_function

from jsondata.jsondata import JSONData
from jsondata.jsonpointer import JSONPointer

# JSON document
jdata = { 'a': { 'b': { 'c': 2, 'd': 3 } } }
  
# JSON branch with array
arr = { 'e': { 'lx': [] } }
  
# Branch elements for array
ai0 = { 'v0': 100}
ai1 = { 'v1': 200}
  
  
# JSON branch with object
obj = { 'f': { 'ox': {} } }
  
# Branch elements for object
l0 = { 'o0': 10}
l1 = { 'o1': 20}
  
  
# JSON in-memory document
D = JSONData(jdata)

print(JSONData(['a', 'b', 'c']))

print(JSONData(JSONPointer('/a/b/c')))

print(JSONData('/a/b/c'))

n = JSONPointer('/a/b/c')(JSONData.data, True)
print(n['c'])

n = JSONPointer('/a/b/c')(JSONData.data, True)
px = fetch_pointerpath(n, JSONData.data)[0]
px.append('c')

print(JSONData(JSONPointer(px)))
