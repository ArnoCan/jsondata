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

from jsondata.jsondata import JSONData
from jsondata.jsonpointer import JSONPointer

class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        
        self.jd = JSONData(
                {
                   'a': {
                      'b': {
                         'c': {
                            'd': [
                               3,
                               4
                            ]
                         }
                      }
                   }
                }
            )

    def testCase000(self):
        jp = JSONPointer('/a/b/1/c/')

        resx = ['a', 'b', 1, 'c', '']
        res = []
        for x in jp.iter_path():
            res.append(x)
        self.assertEqual(res, resx)


    def testCase060(self):

        jpx = JSONPointer("/a/b/c/d/1")

        res = jpx.get_node_value(self.jd)
        assert res == 4

    def testCase070(self):
        res = self.jd('/a/b/c/d/1')
        assert res == 4

    def testCase080(self):
        
        jpx = JSONPointer("/a/b/c/d/1")

        res = self.jd(jpx)
        assert res == 4

    def testCase090(self):
        res = JSONPointer(["a", "b", "c", "d", "1"]).get_node_value(self.jd)
        assert res == 4


if __name__ == '__main__':
    unittest.main()
