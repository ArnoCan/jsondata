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
from jsondata import JSONPointerError

class CallUnits(unittest.TestCase):

    def testCase010(self):
        jp = JSONPointer('/a/b/1/c/')

        data = {'a': {'b': [{'c': 4711}]}}
        resx = ['a', 'b', 1, 'c']
        res = []
        try:
            for x in jp.iter_path_nodes(data):
                res.append(x)
            self.assertEqual(res, resx)
        except JSONPointerError:
            pass

    def testCase020(self):
        jp = JSONPointer('/a/b/0/c/')

        data = {'a': {'b': [{'c': 4711}]}}
        resx = [data['a'], data['a']['b'], data['a']['b'][0], data['a']['b'][0]['c']]
        res = []
        try:
            for x in jp.iter_path_nodes(data):
                res.append(x)
            self.assertEqual(res, resx)
        except JSONPointerError:
            pass


if __name__ == '__main__':
    unittest.main()
