from __future__ import absolute_import
from __future__ import print_function

import sys
import unittest

if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport  @UnusedImport pylint: disable=import-error
else:
    import json as myjson  # @Reimport @UnusedImport
import jsonschema  # @UnusedImport


from jsondata.jsondata import JSONData, \
    JSONDataNodeTypeError, JSONDataKeyError
from jsondata.jsonpointer import JSONPointer


class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.data = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        
    def testCase010(self):
        target = JSONPointer('/a/b/c')
        self.assertTrue(self.data.branch_test(target, 2))

    def testCase020(self):
        target = JSONPointer('/a/b')
        self.assertTrue(self.data.branch_test(target, {'c': 2, 'd': 3}))

    def testCase030(self):
        target = JSONPointer('/a')
        self.assertTrue(self.data.branch_test(target, {'b': {'c': 2, 'd': 3}}))

    def testCase040(self):
        target = JSONPointer('/e')
        self.assertTrue(self.data.branch_test(target, {'lx': [{'v0': 100}, {'v1': 200}]}))

    def testCase050(self):
        target = JSONPointer('/e/lx/0')
        self.assertTrue(self.data.branch_test(target, {'v0': 100}))

    def testCase060(self):
        target = JSONPointer('/e/lx/0/v0')
        self.assertTrue(self.data.branch_test(target, 100))

    def testCase070(self):
        target = JSONPointer('/e/lx/1')
        self.assertTrue(self.data.branch_test(target, {'v1': 200}))

    def testCase080(self):
        target = JSONPointer('/e/lx/1/v1')
        self.assertTrue(self.data.branch_test(target, 200))


if __name__ == '__main__':
    unittest.main()
