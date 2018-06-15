# -*- coding: utf-8 -*-
"""Standards tests from RFC6902 for compliance of patch syntax.

"""
from __future__ import absolute_import

import unittest
import sys


if 'ujson' in sys.argv:
    import ujson as myjsonq  # @UnresolvedImport @UnusedImport pylint: disable=import-error
else:
    import json as myjson  # @UnusedImport

from jsondata.jsondata import JSONData
from jsondata.jsonpointer import JSONPointer

#
#######################
#


class CallUnits(unittest.TestCase):

    def testCase100(self):
        data = {'a': {'b': {'c': 2, 'd': ['a', 'b']}}}
        D = JSONData({})
        n = JSONPointer('0', startrel='/a/b')
        
        self.assertEqual(n.get_pointer_str(superpose=True), '/a/b/')

        x, r = n.get_node_exist(D)
        assert x == {} 
        assert r == None

        D.branch_add(data, x, r)

        assert D.data == data


if __name__ == '__main__':
    unittest.main()
