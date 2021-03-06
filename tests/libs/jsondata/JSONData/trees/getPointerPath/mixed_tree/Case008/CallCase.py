"""Append list element.
"""
from __future__ import absolute_import

import unittest
import os
import sys

# pre-set the base JSON libraries for 'jsondata' by PyUnit call
if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport
elif 'json' in sys.argv:
    import json as myjson
else:
    import json as myjson
import jsonschema

from jsondata import M_ALL
from jsondata.jsondata import JSONData
from jsondata.jsonpointer import JSONPointer, fetch_pointerpath

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
        c0 = [4]

        n3 = [[{'c0': c0},    {'c3': [3]}, [c0]]]
        n4 = {'x0': [[[3], {'c0': c0},    [c0]]]}
        n6 = [[[[n4]]]]
        n7 = [[n4]]
        n8 = {'x': {'c0': c0}}

        sl6 = [n3, n6, n4, n7, n8, ]

        p0 = fetch_pointerpath(n4['x0'][0][2][0], sl6, M_ALL)
        resx = [
            [0, 0, 0, 'c0'],
            [0, 0, 2, 0],
            [1, 0, 0, 0, 0, 'x0', 0, 1, 'c0'],
            [1, 0, 0, 0, 0, 'x0', 0, 2, 0],
            [2, 'x0', 0, 1, 'c0'],
            [2, 'x0', 0, 2, 0],
            [3, 0, 0, 'x0', 0, 1, 'c0'],
            [3, 0, 0, 'x0', 0, 2, 0],
            [4, 'x', 'c0']
        ]
        assert p0 == resx

        pathlst = []
        for rx in resx:
            pathlst.append(JSONPointer(rx).get_pointer())
        pathx = [
            u'/0/0/0/c0',
            u'/0/0/2/0',
            u'/1/0/0/0/0/x0/0/1/c0',
            u'/1/0/0/0/0/x0/0/2/0',
            u'/2/x0/0/1/c0',
            u'/2/x0/0/2/0',
            u'/3/0/0/x0/0/1/c0',
            u'/3/0/0/x0/0/2/0',
            u'/4/x/c0'
        ]
        assert pathlst == pathx

        vallst = []
        for rx in resx:
            vallst.append(JSONPointer(rx).get_node_value(sl6))
        vallstx = [
            [4],
            [4],
            [4],
            [4],
            [4],
            [4],
            [4],
            [4],
            [4]
        ]
        assert vallst == vallstx


if __name__ == '__main__':
    unittest.main()
