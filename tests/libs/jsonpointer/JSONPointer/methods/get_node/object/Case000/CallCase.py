# -*- coding: utf-8 -*-
"""Standards tests from RFC6902 for compliance of patch syntax.

"""
from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson
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
        n = JSONPointer('')
        n = n(D.data)
        D.branch_add(data, n)

        assert D.data == data
        pass


if __name__ == '__main__':
    unittest.main()
