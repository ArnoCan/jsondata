# -*- coding: utf-8 -*-
"""Standards tests from RFC6902 for compliance of patch syntax.

"""
from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
else:
    import json as myjson

try:
    from jsondata.jsonpointer import JSONPointer
    from jsondata.jsondata import JSONData
except Exception as e:
    print("\n#\n#*** Set 'PYTHONPATH' (" + str(e) + ")\n#\n")

#
#######################
#


class CallUnits(unittest.TestCase):

    def testCase100(self):
        data = {'a': {'b': {'c': 2}}}
        D = JSONData({})
        n = JSONPointer('')(D.data)
        D.branch_add(data, n)
        pass

    def testCase101(self):
        data = {'a': {'b': {'c': 2}}}
        D = JSONData({})
        n = JSONPointer('')(D.data)
        D.branch_add(data, n)
        pass

    def testCase011(self):
        data = {'a': {'b': {'c': 2}}}
        D = JSONData(data)
        n = JSONPointer('/a')(D.data)
        D.branch_add(data, n)
        pass

    def testCase012(self):

        data = {'a': {'b': {'c': 2}}}
        D = JSONData(data)
        n = JSONPointer("/a/b/c")
        n = n(D.data, True)
        D.branch_add(data, n)

        assert D.data == {'a': {'b': {'c': 2, 'a': {'b': {'c': 2}}}}}
        pass


if __name__ == '__main__':
    unittest.main()
