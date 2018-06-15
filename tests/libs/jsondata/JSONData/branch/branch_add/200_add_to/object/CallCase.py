"""Append list element.
"""
from __future__ import absolute_import

import unittest
import os
import sys

# pre-set the base JSON libraries for 'jsondata' by PyUnit call
if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
elif 'json' in sys.argv:
    import json as myjson
else:
    import json as myjson
import jsonschema

# import 'jsondata'
from jsondata.jsondataserializer import JSONData
from jsondata import JSONDataNodeTypeError

class CallUnits(unittest.TestCase):

    def testCase000(self):
        D = JSONData({'a': {'b': {'c': 2}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        source = {'d': 3}
        
        D.branch_add(source, D['a']['b'])  #pylint: disable=unsubscriptable-object

        # print(repr(D))
        resx = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}

        self.assertEqual(D, resx)        

    def testCase010(self):
        D = JSONData({'a': {'b': {'c': 2}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        source = {'b': {'c': 2, 'd': 3}}
        
        D.branch_add(source, D['a'])  #pylint: disable=unsubscriptable-object

        # print(repr(D))
        resx = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}

        self.assertEqual(D, resx)        

    def testCase020(self):
        D = JSONData({'a': {}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        source = {'b': {'c': 2, 'd': 3}}
        
        D.branch_add(source, D['a'])  #pylint: disable=unsubscriptable-object

        # print(repr(D))
        resx = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}

        self.assertEqual(D, resx)        

    def testCase030(self):
        D = JSONData({'a': None, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        source = {'b': {'c': 2, 'd': 3}}
        
        try:
            D.branch_add(source, D['a'])  #pylint: disable=unsubscriptable-object
        except JSONDataNodeTypeError:
            pass

    def testCase040(self):
        D = JSONData({'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        source = {'a': {'b': {'c': 2, 'd': 3}}}
        
        D.branch_add(source, D)  #pylint: disable=unsubscriptable-object

        # print(repr(D))
        resx = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}

        self.assertEqual(D, resx)        

    def testCase050(self):
        D = JSONData({'e': {'lx': [{'v0': 100}, {'v1': 200}]}})
        source = {'b': {'c': 2, 'd': 3}}
        
        D.branch_add(source, D, 'a')  #pylint: disable=unsubscriptable-object

        # print(repr(D))
        resx = {'a': {'b': {'c': 2, 'd': 3}}, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}}

        self.assertEqual(D, resx)        


if __name__ == '__main__':
    unittest.main()
