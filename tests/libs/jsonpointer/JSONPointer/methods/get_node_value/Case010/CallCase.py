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

    def testCase010(self):
        sx = JSONPointer('0/a/b').get_node_exist(self.jd)
        assert not sx[1]
        
        x0 = fetch_pointerpath(sx[0], self.jd)
        jpx = JSONPointer('0/c/d/1', startrel=x0[0])

        res = jpx.get_node_value(self.jd)
        self.assertEqual(res, 4)


    def testCase080(self):
        res = JSONPointer(["a", "b", "c", "d", "1"]).get_node_value(self.jd)
        assert res == 4


    def testCase090(self):
        res = JSONPointer("0/c/d/1", startrel=["a", "b"]).get_node_value(self.jd)
        assert res == 4

if __name__ == '__main__':
    unittest.main()
