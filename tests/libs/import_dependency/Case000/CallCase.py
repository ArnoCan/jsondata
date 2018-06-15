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


class CallUnits(unittest.TestCase):

    def testCase100(self):
        data = {'a': 2}
        D = JSONData(data)
        p = JSONPointer('/a')
        eq = p(D.data) == 2
        assert p(D.data) == 2

if __name__ == '__main__':
    unittest.main()
