from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import unittest
import copy

if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport  @UnusedImport pylint: disable=import-error
else:
    import json as myjson  # @Reimport @UnusedImport
import jsonschema  # @UnusedImport

from jsondata.jsondata import JSONData
from jsondata import B_AND, B_OR, B_XOR

class CallUnits(unittest.TestCase):

    def testCase010(self):
        jval = JSONData({"a": 0, "b": 1, "c": [2, 3]})
        jval.branch_superpose(
            {"c": 4},
            map=B_XOR,
            )
        self.assertEqual(jval, {"a": 0, "b": 1, "c": 4})

    def testCase011(self):
        data = {"a": 0, "b": 1, "c": [2, 3]}
        jval = JSONData(data)
        jval.branch_superpose(
            4,
            data['c'],
            2,
            map=B_XOR,
            )
        self.assertEqual(jval, {"a": 0, "b": 1, "c": [2, 3, 4]})

    def testCase012(self):
        jval = JSONData({"a": 0, "b": 1, "c": [2, 3]})
        jval.branch_superpose(
            4,
            '/c',
            2,
            map=B_XOR,
            )
        self.assertEqual(jval, {"a": 0, "b": 1, "c": [2, 3, 4]})

    def testCase013(self):
        jval = JSONData({"a": 0, "b": 1, "c": [2, 3]})
        jval.branch_superpose(
            4,
            '',
            'c',
            map=B_XOR,
            )
        self.assertEqual(jval, {"a": 0, "b": 1, "c": 4})


    def testCase020(self):
        jval = JSONData({"a": 0, "b": 1, "c": [2, 3]})
        jval.branch_superpose(
            {"c": 4.2},
            map=B_XOR,
            )
        self.assertEqual(jval, {"a": 0, "b": 1, "c": 4.2})

    def testCase030(self):
        jval = JSONData({"a": 0, "b": 1, "c": [2, 3]})
        jval.branch_superpose(
            {"c": "dummy"},
            map=B_XOR,
            )
        self.assertEqual(jval, {"a": 0, "b": 1, "c": "dummy"})

if __name__ == '__main__':
    unittest.main()
