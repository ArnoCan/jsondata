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

from jsondata import NOTATION_JSON
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

    def testCase010(self):
        sx = JSONPointer('0/a/b/c/d/0')
        jpx = JSONPointer('3/c/d/1', startrel=sx)

        res0 = jpx.get_startrel()
        self.assertEqual(res0, sx)

        gv = jpx.get_node_value(self.jd)
        self.assertEqual(gv, 4)


if __name__ == '__main__':
    unittest.main()
