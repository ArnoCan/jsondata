"""Append list element.
"""
from __future__ import absolute_import

import unittest
import os
import sys

# pre-set the base JSON libraries for 'jsondata' by PyUnit call 
if 'ujson' in sys.argv:
    import ujson as myjson
elif 'json' in sys.argv:
    import json as myjson
else:
    import json as myjson
import jsonschema

from jsondata.JSONData import JSONData

# name of application, used for several filenames as MODE_SCHEMA_DRAFT4
_APPNAME = "jsondatacheck"
appname = _APPNAME

#
#######################
#
class CallUnits(unittest.TestCase):
    """Base branch_add.
    """
    name=os.path.curdir+__file__

    output=True
    output=False

    def testCase100(self):
        c0 = {'c0': 4}
        n3 = { 'A': {'a0': { 'b0': c0,          'b1': {'c0': 3}, 'b2': c0 }}}
        n4 = { 'B': {'a0': { 'b0': { 'c0': 2 }, 'b1': c0,        'b2': c0 }}}
        n6 = { 'x0': { 'x1': { 'x2': n4 }} }
        n7 = { 'y0': { 'y1': n4 }}
        n8 = { 'y0': { 'y1': c0 }}
         
        sl6 = [ n3, n6, n4, n7, n8, ]
         
        p0 = JSONData.getPointerPath(n4['B']['a0']['b2']['c0'],sl6,JSONData.ALL)
        resx = [
            [0, 'A', 'a0', 'b0', 'c0'], 
            [0, 'A', 'a0', 'b2', 'c0'], 
            [1, 'x0', 'x1', 'x2', 'B', 'a0', 'b1', 'c0'], 
            [1, 'x0', 'x1', 'x2', 'B', 'a0', 'b2', 'c0'], 
            [2, 'B', 'a0', 'b1', 'c0'], 
            [2, 'B', 'a0', 'b2', 'c0'], 
            [3, 'y0', 'y1', 'B', 'a0', 'b1', 'c0'], 
            [3, 'y0', 'y1', 'B', 'a0', 'b2', 'c0'], 
            [4, 'y0', 'y1', 'c0']
        ]
        assert p0 == resx


#     def testCase500(self):
#         """Equal."""
#         n0 = { 'a0': { 'b0': { 'c0': 2 }, 'b1': {'c0': 3}, 'b2': {'c0': 4} }}
#         n1 = { 'a0': { 'b0': { 'c0': 2 }, 'b1': {'c0': 3}, 'b2': {'c0': 4} }}
#         n2 = { 'a0': { 'b0': { 'c0': 2 }, 'b1': {'c0': 3}, 'b2': {'c0': 4} }}
#         
#         n3 = { 'A': {'a0': { 'b0': { 'c0': 2 }, 'b1': {'c0': 3}, 'b2': {'c0': 4} }}}
#         n4 = { 'B': {'a0': { 'b0': { 'c0': 2 }, 'b1': {'c0': 3}, 'b2': {'c0': 4} }}}
#         
#         n5 = { 'x': 12 }
# 
#         sl0 = [ n0, n1, n2, n3, n4, ]
#         sl1 = [ n0, n1, n2 ]
#         sl2 = [ n0, n2, n3, n4, ]
#         sl3 = [ n0, n3, n4, ]
#         sl4 = [ n3, n4, ]
#         sl5 = [ n5, ]
#         
#         res = []
#         
#         p0 = JSONData.getPointerPath(n5,sl5)
#         resx = [[0]]
#         assert p0 == resx
#         pass


if __name__ == '__main__':
    unittest.main()
