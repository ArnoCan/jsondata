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

        jp = JSONPointer('')  # see rfc6901 - section 5 / pg. 5
        res = jp(self.jd)

        assert res == self.jd


    def testCase010(self):

        jp = JSONPointer("/")  # see rfc6901 - section 5 / pg. 5
        res = jp(self.jd)

        assert res == 0


if __name__ == '__main__':
    unittest.main()
