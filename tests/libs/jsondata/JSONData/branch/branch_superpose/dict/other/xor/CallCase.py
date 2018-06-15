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
            map=B_XOR,
            )
        self.assertEqual(jval, {"a": 0, "b": 1, "c": [2, 3]})

    def testCase020(self):
        jval = JSONData({"a": 0, "b": 1, "c": [2, 3]})
        jval.branch_superpose(
            4.2,
            map=B_XOR,
            )
        self.assertEqual(jval, {"a": 0, "b": 1, "c": [2, 3]})

    def testCase030(self):
        jval = JSONData({"a": 0, "b": 1, "c": [2, 3]})
        jval.branch_superpose(
            "dummy",
            map=B_XOR,
            )
        self.assertEqual(jval, {"a": 0, "b": 1, "c": [2, 3]})

    def testCase040(self):
        jval = JSONData({"a": 0, "b": 1, "c": [2, 3]})
        jval.branch_superpose(
            ["dummylist"],
            map=B_XOR,
            )
        self.assertEqual(jval, {"a": 0, "b": 1, "c": [2, 3]})

    def testCase110(self):
        jval = JSONData({})
        jval.branch_superpose(
            4,
            map=B_XOR,
            )
        self.assertEqual(jval, {})

    def testCase120(self):
        jval = JSONData({})
        jval.branch_superpose(
            4.2,
            map=B_XOR,
            )
        self.assertEqual(jval, {})

    def testCase130(self):
        jval = JSONData({})
        jval.branch_superpose(
            "dummy",
            map=B_XOR,
            )
        self.assertEqual(jval, {})

    def testCase140(self):
        jval = JSONData({})
        jval.branch_superpose(
            ["dummylist"],
            map=B_XOR,
            )
        self.assertEqual(jval, {})

    def testCase210(self):
        jval = JSONData([])
        jval.branch_superpose(
            4,
            map=B_XOR,
            )
        self.assertEqual(jval, {})

    def testCase220(self):
        jval = JSONData([])
        jval.branch_superpose(
            4.2,
            map=B_XOR,
            )
        self.assertEqual(jval, [])

    def testCase230(self):
        jval = JSONData([])
        jval.branch_superpose(
            "dummy",
            map=B_XOR,
            )
        self.assertEqual(jval, [])

    def testCase240(self):
        jval = JSONData([])
        jval.branch_superpose(
            ["dummylist"],
            map=B_XOR,
            )
        self.assertEqual(jval, ["dummylist"])

    def testCase310(self):
        jval = JSONData(None)
        jval.branch_superpose(
            4,
            map=B_XOR,
            )
        self.assertEqual(jval, 4)

    def testCase320(self):
        jval = JSONData(None)
        jval.branch_superpose(
            4.2,
            map=B_XOR,
            )
        self.assertEqual(jval, 4.2)

    def testCase330(self):
        jval = JSONData(None)
        jval.branch_superpose(
            "dummy",
            map=B_XOR,
            )
        self.assertEqual(jval, "dummy")

    def testCase340(self):
        jval = JSONData(None)
        jval.branch_superpose(
            ["dummylist"],
            map=B_XOR,
            )
        self.assertEqual(jval, ["dummylist"])

    def testCase410(self):
        jval = JSONData('')
        jval.branch_superpose(
            4,
            map=B_XOR,
            )
        self.assertEqual(jval, '')

    def testCase420(self):
        jval = JSONData('')
        jval.branch_superpose(
            4.2,
            map=B_XOR,
            )
        self.assertEqual(jval, '')

    def testCase430(self):
        jval = JSONData('')
        jval.branch_superpose(
            "dummy",
            map=B_XOR,
            )
        self.assertEqual(jval, '')

    def testCase440(self):
        jval = JSONData('')
        jval.branch_superpose(
            ["dummylist"],
            map=B_XOR,
            )
        self.assertEqual(jval, '')

if __name__ == '__main__':
    unittest.main()
