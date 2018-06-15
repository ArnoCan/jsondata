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
        jval = JSONData({"a": 0, "b": 1, "c": {"x": 2, "y": 3}})
        jval.branch_superpose(
            {"c": {"z": 4}},
            # default: map=B_OR,
            )
        self.assertEqual(jval, {"a": 0, "b": 1, "c": {"x": 2, "y": 3, "z": 4}})

    def testCase020(self):
        jval = JSONData({"a": 0, "b": 1, "c": {"x": 2, "y": 3}})
        jval.branch_superpose(
            {"c": {"z": 4}},
            map=B_OR,
            )
        self.assertEqual(jval, {"a": 0, "b": 1, "c": {"x": 2, "y": 3, "z": 4}})

    def testCase030(self):
        jval = JSONData({"a": 0, "b": 1, "c": {"x": 2, "y": 3}})
        jval.branch_superpose(
            {"c": {"x": 11, "y": 22, "z": 4}},
            map=B_XOR,
            )
        
        self.assertEqual(jval, {"a": 0, "b": 1, "c": {"x": 2, "y": 3, "z": 4}})

    def testCase040(self):
        jval = JSONData({"a": 0, "b": 1, "c": {"x": 2, "y": 3}})
        jval.branch_superpose(
            {"c": {"x": 11, "y": 22, "z": 4}},
            map=B_AND,
            )
        
        self.assertEqual(jval, {"a": 0, "b": 1, "c": {"x": 11, "y": 22}})

if __name__ == '__main__':
    unittest.main()
