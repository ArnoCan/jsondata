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

    def testCase000(self):
        sx = JSONPointer('/a/b').get_node_exist(self.jd)
        assert not sx[1]
        sx = fetch_pointerpath(sx[0], self.jd)

        jpx = JSONPointer('0/c/d/1', startrel=sx[0])

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

    def testCase020(self):
        sx = JSONPointer('0/a/b')
        jpx = JSONPointer('0/1/c/', startrel=sx)

        resx = "/a/b/1/c/"
        res = str(jpx)
        self.assertEqual(res, resx)


    def testCase050(self):
        jp = JSONPointer('0/1/c/', startrel='0/a/b')

        resx = ['a', 'b', 1, 'c', '']
        res = []
        for x in jp.iter_path():
            res.append(x)
        self.assertEqual(res, resx)


    def testCase060(self):

        jpx = JSONPointer("0/a/b/c/d/1")

        res = jpx.get_node_value(self.jd)
        assert res == 4

    def testCase070(self):
        res = self.jd('0/a/b/c/d/1')
        assert res == 4

    def testCase080(self):
        
        jpx = JSONPointer("0/a/b/c/d/1")

        res = self.jd(jpx)
        assert res == 4

    def testCase090(self):
        res = JSONPointer(["a", "b", "c", "d", "1"]).get_node_value(self.jd)
        assert res == 4


if __name__ == '__main__':
    unittest.main()
