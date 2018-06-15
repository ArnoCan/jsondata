from __future__ import absolute_import
from __future__ import print_function

import sys
import unittest

sys.tracebacklimit = 1000

if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport  @UnusedImport pylint: disable=import-error
else:
    import json as myjson  # @Reimport @UnusedImport
import jsonschema  # @UnusedImport

from jsondata import M_ALL, JSONDataParameterError
from jsondata.jsondata import JSONData
from jsondata.jsonpointer import JSONPointer, fetch_pointerpath

class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        
        self.jd = JSONData(
                {
                   "a": {
                      "b": {
                         "c": {
                            "d": [
                               3,
                               4
                            ]
                         }
                      }
                   },
                   "": 0
                }
            )

    def testCase050(self):
        jp = JSONPointer('0/1/c/', startrel='0/a/b')

        resx = ['a', 'b', 1, 'c', '']
        res = []
        for x in jp.iter_path():
            res.append(x)
        self.assertEqual(res, resx)

    def testCase060(self):
        jp = JSONPointer('0/1/c/', startrel='0/a/b')

        resx = [1, 'c', '']
        res = []
        for x in jp.iter_path(superpose=False):
            res.append(x)
        self.assertEqual(res, resx)

    def testCase070(self):
        jp = JSONPointer('0/1/c', startrel='0/a/b')

        resx = [1, 'c']
        res = []
        for x in jp.iter_path(superpose=False):
            res.append(x)
        self.assertEqual(res, resx)

if __name__ == '__main__':
    unittest.main()
