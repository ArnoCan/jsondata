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

from jsondata import M_ALL
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
        
        data = {
            0: {'a': 'pattern'},
            1: [{'x':[{'a': 'pattern'}]}]
        }
        nx = data[1][0]['x'][0]
        res = fetch_pointerpath(nx, data)
        resx = [
          [1, 0, 'x', 0]
        ]
        assert res == resx

    def testCase020(self):

        n = {'a': 'pattern'}
        data = {
            5: n,
            6: [{'x':[n]}],
            7: [[3, {'x':[n]}]]
        }
        res = fetch_pointerpath(n, data, M_ALL)
        resx = [
            [5],
            [6, 0, 'x', 0],
            [7, 0, 1, 'x', 0]
        ]
        assert res == resx

    def testCase030(self):

        n = {'a': 'pattern'}
        data = [
            {5: n},
            {6: [{'x':[n]}]},
            {7: [[3, {'x':[n]}]]}
        ]
        res = fetch_pointerpath(n, data, M_ALL)
        resx = [
            [0, 5],
            [1, 6, 0, 'x', 0],
            [2, 7, 0, 1, 'x', 0]
        ]
        assert res == resx

    def testCase040(self):

        n = {'a': 'pattern'}
        data = [
            [5, n],
            [6, [n]],
            [7, [[3, [n]]]]
        ]
        res = fetch_pointerpath(n, data, M_ALL)
        resx = [
            [0, 1],
            [1, 1, 0],
            [2, 1, 0, 1, 0]
        ]
        assert res == resx

    def testCase100(self):
        sx = JSONPointer('0/a/b').get_node_exist(self.jd)
        assert not sx[1]
        
        resx = [['a', 'b']]
        res = fetch_pointerpath(sx[0], self.jd)
        assert res == resx


if __name__ == '__main__':
    unittest.main()
