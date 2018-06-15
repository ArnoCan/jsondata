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

    def testCase011(self):
        target = JSONPointer('0/c', startrel='/a/b')
        self.assertTrue(self.data.branch_test(target, 2))

    def testCase012(self):
        target = JSONPointer('1/c', startrel='/a/b/c')
        self.assertTrue(self.data.branch_test(target, 2))

    def testCase013(self):
        target = JSONPointer('0', startrel='/a/b/c')
        self.assertTrue(self.data.branch_test(target, 2))

    def testCase020(self):
        target = JSONPointer('/a/b')
        self.assertTrue(self.data.branch_test(target, {'c': 2, 'd': 3}))

    def testCase021(self):
        target = JSONPointer('0', startrel='/a/b')
        self.assertTrue(self.data.branch_test(target, {'c': 2, 'd': 3}))

    def testCase030(self):
        target = JSONPointer('/a')
        self.assertTrue(self.data.branch_test(target, {'b': {'c': 2, 'd': 3}}))

    def testCase031(self):
        target = JSONPointer('0', startrel='/a')
        self.assertTrue(self.data.branch_test(target, {'b': {'c': 2, 'd': 3}}))

    def testCase040(self):
        target = JSONPointer('/e')
        self.assertTrue(self.data.branch_test(target, {'lx': [{'v0': 100}, {'v1': 200}]}))

    def testCase041(self):
        target = JSONPointer('0', startrel='/e')
        self.assertTrue(self.data.branch_test(target, {'lx': [{'v0': 100}, {'v1': 200}]}))

if __name__ == '__main__':
    unittest.main()
