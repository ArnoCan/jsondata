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
        target = JSONPointer('/a/b')
        sourcenode = {'alternate': 4711 }

        D.branch_replace(sourcenode, target, 'd')

        resx = {'a': {'b': {'c': 2, 'd': {'alternate': 4711 }}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        self.assertEqual(D, resx)

    def testCase020(self):
        # JSON document
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        sourcenode = {'alternate': 4711 }

        D.branch_replace(sourcenode, JSONPointer('/a/b/c'))

        resx = {'a': {'b': {'c': {'alternate': 4711 }, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        self.assertEqual(D, resx)

    def testCase030(self):
        # JSON document
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        sourcenode = {'alternate': 4711 }

        try:
            D.branch_replace(sourcenode, JSONPointer('/a/b/c'), 'f')
        except JSONDataNodeTypeError:
            pass

    def testCase040(self):
        # JSON document
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        sourcenode = {'alternate': 4711 }

        try:
            D.branch_replace(sourcenode, D['a']['b']['c'], 'f')  #pylint: disable=unsubscriptable-object
        except JSONDataNodeTypeError:
            pass

    def testCase050(self):
        # JSON document
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        sourcenode = {'alternate': 4711 }

        try:
            D.branch_replace(sourcenode, D['a']['b'], 'f')  #pylint: disable=unsubscriptable-object
        except JSONDataNodeTypeError:
            pass

    def testCase060(self):
        # JSON document
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        target = JSONPointer('/a/b')
        sourcenode = {'alternate': 4711 }

        try:
            D.branch_replace(sourcenode, target, 'f')
        except JSONDataKeyError:
            pass

if __name__ == '__main__':
    unittest.main()
