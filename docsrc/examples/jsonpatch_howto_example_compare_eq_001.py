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
  
  
# Add a branch with an array
D.branch_add(JSONPointer('/a/b'),'e',arr['e'])
  
# Add a items to the new array
# Remark: for '-' refer to RFC6901 - array-index
D.branch_add(JSONPointer('/a/b/e/lx'),'-',ai0)
D.branch_add(JSONPointer('/a/b/e/lx'),'-',ai1)
  
  
# Add a branch with an object
D.branch_add(JSONPointer('/a/b'),'f',obj['f'])
  
# Add an item to the new object, from an object
D.branch_add(JSONPointer('/a/b/f/ox'),'v0',ai0['v0'])
  
# Add an item to the new object
ai1v1 = ai1['v1']
D.branch_add(JSONPointer('/a/b/f/ox'),'v1',ai1v1)


nodex = JSONPointer(['a','b'])(D.data)
ret = D.branch_create(nodex, ['g','x'], {})

ret['x0'] = 22
ret['x1'] = 33
  
ret = D.branch_create(nodex, ['g','x','xlst'], [])

ret.append('first')
ret.append('second')

# reference data
rdata = {
    'a': {
        'b': {
            'c': 2,
            'e': {
                'lx': [
                    {'v0': 100}, 
                    {'v1': 200}
                ]
            }, 
            'd': 3,
            u'g': {
                u'x': {
                    'x0': 22,
                    'x1': 33, 
                    u'xlst': [
                        'first',
                        'second'
                    ]
                }
            }, 
            'f': {
                'ox': {
                    'v0': 100,
                    'v1': 200
                }
            }
        }
    }
}

assert D.data == rdata
assert D == rdata

print(D)
