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
        branchpath = ['1', '2', '3', '4', '5', '6']
        target = JSONPointer('')

        D.branch_create(branchpath, target, 'new-value')

        resx = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]},
                '1': {'2': {'3': {'4': {'5': {'6': 'new-value'}}}}}}
        
        self.assertEqual(D, resx)

    def testCase011(self):
        # JSON document
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        branchpath = ['1', '2', '3', '4', '5', '6']
        target = JSONPointer('')

        D.branch_create(branchpath, target, 'new-value')

        resx = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]},
                '1': {'2': {'3': {'4': {'5': {'6': 'new-value'}}}}}}
        
        self.assertEqual(D, resx)

    def testCase012(self):
        # JSON document
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        branchpath = ['1', '2', '3', '4', '5', '6']
        target = JSONPointer('/')

        b = JSONPointer('/')
        t = JSONPointer('')
        D.branch_create(b, t, {})

        D.branch_create(branchpath, target, 'new-value')

        resx = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]},
                '': {'1': {'2': {'3': {'4': {'5': {'6': 'new-value'}}}}}}}
        
        self.assertEqual(D, resx)

    def testCase020(self):
        # JSON document
        D = JSONData({'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        new_path = JSONPointer('/x/y/z')

        D.branch_create(new_path, JSONPointer('/a'))
        resx = {'a': {'b': {'c': 2, 'd': 3},
                      'x': {'y': {'z': None}}},
                'e': {'lx': [{'v0': 100}, {'v1': 200}]}}

        eq = D == resx

        self.assertEqual(D, resx)

    def testCase030(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)
        new_path = JSONPointer('/x/a/b')

        opt_value = JSONPointer('/e/lx/1')(arg)

        D.branch_create(new_path, JSONPointer(''), opt_value)
        
        self.assertEqual(D, arg)

    def testCase031(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)

        new_path = JSONPointer('/x/a/b')
        target = JSONPointer('/')
        opt_value = JSONPointer('/e/lx/1')(arg)

        try:
            D.branch_create('/', JSONPointer(''), '')
            D.branch_create(new_path, target, opt_value)
        except JSONDataNodeTypeError as e:
            # print("4TEST:" + str(e))
            pass
        else:
            raise JSONDataNodeTypeError()

    def testCase032(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)

        new_path = JSONPointer('/x/a/b')
        target = JSONPointer('/')
        opt_value = JSONPointer('/e/lx/1')(arg)

        D.branch_create('/', JSONPointer(''), {})
        D.branch_create(new_path, target, opt_value)
        
        self.assertEqual(D, arg)

    def testCase033(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)

        new_path = JSONPointer('/x/a/b')
        target = JSONPointer('/')
        opt_value = JSONPointer('/e/lx/1')(arg)

        try:
            D.branch_create('/', JSONPointer(''), [])
            D.branch_create(new_path, target, opt_value)
        except JSONDataNodeTypeError as e:
            # print("4TEST:" + str(e))
            pass
        else:
            raise JSONDataNodeTypeError("")

        self.assertEqual(D, arg)

    def testCase034(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)

        new_path = JSONPointer('/0/x/a/b')
        target = JSONPointer('/')
        opt_value = JSONPointer('/e/lx/1')(arg)

        D.branch_create('/', JSONPointer(''), [])
        D.branch_create(new_path, target, opt_value)

        self.assertEqual(D, arg)

    def testCase035(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)

        new_path = JSONPointer('/-/x/a/b')
        target = JSONPointer('/')
        opt_value = JSONPointer('/e/lx/1')(arg)

        D.branch_create('/', JSONPointer(''), [])
        D.branch_create(new_path, target, opt_value)
        
        self.assertEqual(D, arg)

    def testCase040(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        new_path = JSONPointer('/x/y')
        D = JSONData(arg)

        D.branch_create(new_path, D['a']['b'], 4711)  #pylint: disable=unsubscriptable-object

        self.assertEqual(D, arg)

    def testCase050(self):
        # JSON document
        arg = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}
        D = JSONData(arg)
        source = JSONPointer('/a/b')

        try:
            D.branch_create(source, D['a']['b'], 'f')  #pylint: disable=unsubscriptable-object
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
            D.branch_create(source, target, 'f')
        except JSONDataKeyError:
            pass
        self.assertEqual(D, arg)

if __name__ == '__main__':
    unittest.main()
