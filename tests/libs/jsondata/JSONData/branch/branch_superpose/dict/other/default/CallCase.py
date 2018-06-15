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
            4,
            # default: map=B_OR,
            )
        self.assertEqual(jval, 4)

    def testCase020(self):
        jval = JSONData({"a": 0, "b": 1, "c": [2, 3]})
        jval.branch_superpose(
            4.2,
            # default: map=B_OR,
            )
        self.assertEqual(jval, 4.2)

    def testCase030(self):
        jval = JSONData({"a": 0, "b": 1, "c": [2, 3]})
        jval.branch_superpose(
            "dummy",
            # default: map=B_OR,
            )
        self.assertEqual(jval, "dummy")

    def testCase040(self):
        jval = JSONData({"a": 0, "b": 1, "c": [2, 3]})
        jval.branch_superpose(
            ["dummylist"],
            # default: map=B_OR,
            )
        self.assertEqual(jval, ["dummylist"])

if __name__ == '__main__':
    unittest.main()
