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

    def testCase010(self):
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        
        sourcenode = JSONPointer('/e/lx/0/v0')
        target = JSONPointer('/a/b')
        key = 'v0'
        D.branch_move(sourcenode, target, key)

        resx = {'a': {'b': {'c': 2, 'd': 3, 'v0': 100}}, 'e': {'lx': [{}, {'v1': 200}]}}
        self.assertEqual(D, resx)

    def testCase011(self):
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        
        sourcenode = JSONPointer('/e/lx/0/v0')
        target = JSONPointer('/a/b')
        D.branch_move(sourcenode, target)

        resx = {'a': {'b': 100}, 'e': {'lx': [{}, {'v1': 200}]}}
        self.assertEqual(D, resx)

    def testCase012(self):
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        
        sourcenode = JSONPointer('/e/lx/0')
        target = JSONPointer('/a/b')
        D.branch_move(sourcenode, target)

        resx = {'a': {'b': {'v0': 100}}, 'e': {'lx': [{'v1': 200}]}}
        self.assertEqual(D, resx)

    def testCase013(self):
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})

        sourcenode = JSONPointer('/e/lx/0')
        target = JSONPointer('/a/b')
        key = 'v0'

        D.branch_move(sourcenode, target, key)

        resx = {'a': {'b': {'c': 2, 'd': 3, 'v0': {'v0': 100}}}, 'e': {'lx': [{'v1': 200}]}}
        self.assertEqual(D, resx)


if __name__ == '__main__':
    unittest.main()
