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

    def testCase000(self):
        sx = JSONPointer('/a/b')
        jpx = JSONPointer('0/c/d/1', startrel=sx)

        resx = "/a/b/c/d/1"
        res = str(jpx)
        self.assertEqual(res, resx)
        self.assertEqual(jpx(self.jd), 4)

    def testCase001(self):
        sx = JSONPointer('0/a/b')
        jpx = JSONPointer('0/c/d/1', startrel=sx)

        resx = "/a/b/c/d/1"
        res = str(jpx)
        self.assertEqual(res, resx)
        self.assertEqual(jpx(self.jd), 4)

    def testCase002(self):
        sx = JSONPointer('0/a/b/c')
        jpx = JSONPointer('1/c/d/1', startrel=sx)

        resx = "/a/b/c/d/1"
        res = str(jpx)
        self.assertEqual(res, resx)
        self.assertEqual(jpx(self.jd), 4)

    def testCase003(self):
        sx = JSONPointer('/a/b/c')
        jpx = JSONPointer('1/c/d/1', startrel=sx)

        resx = "/a/b/c/d/1"
        res = str(jpx)
        self.assertEqual(res, resx)
        self.assertEqual(jpx(self.jd), 4)

    def testCase004(self):
        sx = JSONPointer('0/a/b/c/0')
        jpx = JSONPointer('2/c/d/1', startrel=sx)

        resx = "/a/b/c/d/1"
        res = str(jpx)
        self.assertEqual(res, resx)
        self.assertEqual(jpx(self.jd), 4)
    
    def testCase005(self):
        sx = JSONPointer('0/a/b/c/0')
        jpx = JSONPointer('2/c/d/1', startrel=sx)

        resx = "/a/b/c/d/1"
        res = str(jpx)
        self.assertEqual(res, resx)
        self.assertEqual(jpx.get_node(self.jd), 4)


if __name__ == '__main__':
    unittest.main()
