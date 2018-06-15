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
        new_path = ['q', 'w', 'e', 'r', 't', 'z']
        target = JSONPointer('')

        D.branch_create(new_path, target, 'new-value')

        resx = {'a': {'b': {'c': 2, 'd': 3}},
                'e': {'lx': [{'v0': 100}, {'v1': 200}]}, 
                'q': {'w': {'e': {'r': {'t': {'z': 'new-value'}}}}}}
        self.assertEqual(D, resx)

    def testCase020(self):
        # JSON document
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        new_path =  JSONPointer('/x')
        target = JSONPointer('/a')

        D.branch_create(new_path, target)

        resx = {'a': {'b': {'c': 2, 'd': 3}, 'x': None}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        self.assertEqual(D, resx)

    def testCase030(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)
        new_path =  JSONPointer('/x')
        target = JSONPointer('/a')
        key = 'f'
        try:
            D.branch_create(new_path, target, key)
        except JSONDataNodeTypeError:
            pass
        self.assertEqual(D, arg)

    def testCase040(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)
        new_path =  JSONPointer('/x')
        target = D['a']['b']['c']  #pylint: disable=unsubscriptable-object
        key = 'f'

        D = JSONData(arg)

        try:
            D.branch_create(new_path, target, key)
        except JSONDataNodeTypeError:
            pass
        self.assertEqual(D, arg)

    def testCase050(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)
        new_path =  JSONPointer('/x')
        target = D['a']['b']  #pylint: disable=unsubscriptable-object
        key = 'f'

        D = JSONData(arg)

        try:
            D.branch_create(new_path, target, key)
        except JSONDataKeyError:
            pass
        self.assertEqual(D, arg)

    def testCase060(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)
        new_path =  JSONPointer('/x')
        target = D['a']
        key = 'f'
        D = JSONData(arg)

        try:
            D.branch_create(new_path, target, key)
        except JSONDataKeyError:
            pass
        self.assertEqual(D, arg)

if __name__ == '__main__':
    unittest.main()
