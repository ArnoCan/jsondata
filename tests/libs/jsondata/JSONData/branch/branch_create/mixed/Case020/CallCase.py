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
        new_path = ['q', '-', 'w', 0, 'e', '-', 'r', '-', 't', '-', 'z', '-']
        target = JSONPointer('')

        D.branch_create(new_path, target, 'new-value')

        resx = {'a': {'b': {'c': 2, 'd': 3}},
                'e': {'lx': [{'v0': 100}, {'v1': 200}]},
                'q': [{'w': [{'e': [{'r': [{'t': [{'z': ['new-value']}]}]}]}]}]}

        # print(repr(D))

        self.assertEqual(D, resx)

    def testCase020(self):
        # JSON document
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        new_path = JSONPointer('/x/a/b')

        D.branch_create(new_path, JSONPointer(''))

        resx = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}, 'x': {'a': {'b': None}}}

        # print(repr(D))

        self.assertEqual(D, resx)

    def testCase030(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)

        new_path = JSONPointer('/a/b')
        target_hook = JSONPointer('')
        optional_padding_value = {'f': False}

        D.branch_create(new_path, target_hook, optional_padding_value)

        resx = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}

        # print(repr(D))

        self.assertEqual(D, resx)

    def testCase040(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        new_path = JSONPointer('/a/b')
        D = JSONData(arg)

        try:
            D.branch_create(new_path, D['a']['b']['c'], 'f')  #pylint: disable=unsubscriptable-object
        except JSONDataNodeTypeError:
            pass

        #print(repr(D))
        #self.assertEqual(D, arg)

    def testCase050(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)
        new_path = JSONPointer('/a/b')

        try:
            D.branch_create(new_path, D['a']['b'], 'f')  #pylint: disable=unsubscriptable-object
        except JSONDataKeyError:
            pass
        self.assertEqual(D, arg)

    def testCase060(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)
        target_hook = JSONPointer('/a/b')
        new_path = JSONPointer('/a/b')
        optional_padding_value = {'f': False}

        D.branch_create(new_path, target_hook, optional_padding_value)

        self.assertEqual(D, arg)

if __name__ == '__main__':
    unittest.main()
