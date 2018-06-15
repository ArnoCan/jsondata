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
        # JSON document
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        source = JSONPointer('/a/b')
        target = JSONPointer('')

        D.branch_copy(source, target, 'x')

        resx = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}, 'x': {'c': 2, 'd': 3}}
        self.assertEqual(D, resx)

    def testCase020(self):
        # JSON document
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        source = JSONPointer('/a/b')

        D.branch_copy(source, JSONPointer('/x'))

        resx = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}, 'x': {'c': 2, 'd': 3}}
        self.assertEqual(D, resx)

    def testCase030(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)
        source = JSONPointer('/a/b')

        try:
            D.branch_copy(source, JSONPointer('/x'), 'f')
        except JSONDataKeyError:
            pass
        self.assertEqual(D, arg)

    def testCase040(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        source = JSONPointer('/a/b')
        D = JSONData(arg)

        try:
            D.branch_copy(source, D['a']['b']['c'], 'f')  #pylint: disable=unsubscriptable-object
        except JSONDataNodeTypeError:
            pass

    def testCase050(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)
        source = JSONPointer('/a/b')

        try:
            D.branch_copy(source, D['a']['b'], 'f')  #pylint: disable=unsubscriptable-object
        except JSONDataKeyError:
            pass
        self.assertEqual(D, arg)

    def testCase060(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)
        target = JSONPointer('/a/b')
        source = JSONPointer('/a/b')

        try:
            D.branch_copy(source, target, 'f')
        except JSONDataKeyError:
            pass
        self.assertEqual(D, arg)

if __name__ == '__main__':
    unittest.main()
