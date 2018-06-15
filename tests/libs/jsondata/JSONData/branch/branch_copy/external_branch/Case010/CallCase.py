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
        source = {'q': 'w', 'e': 'r', 't': 'z'}
        target = JSONPointer('')

        D.branch_copy(source, target, 'x')

        resx = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}, 'x': {'q': 'w', 'e': 'r', 't': 'z'}}
        self.assertEqual(D, resx)

    def testCase020(self):
        # JSON document
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        source = {'q': 'w', 'e': 'r', 't': 'z'}

        D.branch_copy(source, JSONPointer('/x'))

        resx = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}, 'x': {'q': 'w', 'e': 'r', 't': 'z'}}
        self.assertEqual(D, resx)

    def testCase030(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)
        source = {'q': 'w', 'e': 'r', 't': 'z'}

        D.branch_copy(source, JSONPointer(''), 'f')
        
        resx = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}, 'f': {'q': 'w', 'e': 'r', 't': 'z'}}
        self.assertEqual(D, resx)

    def testCase040(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        source = {'q': 'w', 'e': 'r', 't': 'z'}
        D = JSONData(arg)

        try:
            D.branch_copy(source, D['a']['b']['c'], 'f')  #pylint: disable=unsubscriptable-object
        except JSONDataNodeTypeError:
            pass

    def testCase050(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        source = {'q': 'w', 'e': 'r', 't': 'z'}
        D = JSONData(arg)

        D.branch_copy(source, D['a']['b'], 'f')  #pylint: disable=unsubscriptable-object
        resx = {'a': {'b': {'c': 2, 'f': {'q': 'w', 'e': 'r', 't': 'z'}, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}, }

        self.assertEqual(D, resx)

    def testCase060(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)
        target = JSONPointer('/a/b')
        source = {'q': 'w', 'e': 'r', 't': 'z'}

        D.branch_copy(source, target, 'f')

        resx = {'a': {'b': {'c': 2, 'd': 3, 'f': {'q': 'w', 'e': 'r', 't': 'z'}}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        self.assertEqual(D, resx)

if __name__ == '__main__':
    unittest.main()
