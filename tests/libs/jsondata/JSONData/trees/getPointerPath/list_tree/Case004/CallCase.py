"""Append list element.
"""
from __future__ import absolute_import

import unittest
import os
import sys

# pre-set the base JSON libraries for 'jsondata' by PyUnit call
if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
elif 'json' in sys.argv:
    import json as myjson
else:
    import json as myjson
import jsonschema

from jsondata.jsonpointer import JSONPointer, fetch_pointerpath
from jsondata import M_FIRST
# name of application, used for several filenames as MS_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME

#
#######################
#


class CallUnits(unittest.TestCase):
    """Base branch_add.
    """

    def testCase100(self):
        n3 = [[[[2], [[3]], [[4]]]]]
        n4 = [[[[3], [[4]], [[5]]]]]
        n6 = [[[[n4]]]]
        sl6 = [n3, n6, n4, ]

        a = n4[0][0][2]
        assert n4[0][0][2] == [[5]]

        p0 = fetch_pointerpath(n4[0][0][2], n4)
        resx = [[0, 0, 2]]
        assert p0 == resx

        p0 = fetch_pointerpath(n4[0][0][2], sl6)
        resx = [[1, 0, 0, 0, 0, 0, 0, 2]]
        assert p0 == resx

        p0 = fetch_pointerpath(n4[0][0][2], sl6, M_FIRST)
        resx = [[1, 0, 0, 0, 0, 0, 0, 2]]
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
#         p0 = fetch_pointerpath(n5,sl5)
#         resx = [[0]]
#         assert p0 == resx
#         pass


if __name__ == '__main__':
    unittest.main()
