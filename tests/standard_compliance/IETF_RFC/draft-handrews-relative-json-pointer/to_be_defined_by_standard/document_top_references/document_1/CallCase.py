# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson
else:
    import json as myjson
import jsonschema


jval = None

from jsondata import JSONPointerError
from jsondata.jsondata import JSONData
from jsondata.jsonpointer import JSONPointer
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF

# name of application, used for several filenames as MS_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME


class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        
        self.refx = {
            "x": 2,
            "a": [3, 4]
        }

        self.data = JSONData(self.refx)

    def testCase100(self):
        self.tstOK = [
            #Starting value          Starting                        Relative JSON Pointer           result
            #------------------------------------------------------------------------------------------------------
            (self.refx["x"],         "",                            "0/x",                           2,),
            (self.refx["x"],         "/x",                          "0#",                            "x",),
            (self.refx["x"],         "/x",                          "0",                             2,),
        ]
        dbgcnt = 0
        for tst in self.tstOK:
            try:
                startrel = JSONPointer(tst[2], startrel=tst[1])
                
#                 print("4TEST:" + str(startrel))
#                 print("4TEST:" + repr(startrel))
#                 print("4TEST:" + str(startrel.get_startrel()))
#                 print("4TEST:" + str(startrel.get_start()))
#                 print("4TEST:" + repr(startrel.get_startrel()))
#                 print("4TEST:" + repr(startrel.get_start()))

                #res = startrel.evaluate(self.data)
                res = startrel(self.data)
                self.assertEqual(res, tst[3])
                dbgcnt += 1
            except Exception as e:
                raise Exception(
                    str(e)
                    + "\n" + str(tst)
                    )  # from None

    def testCase200(self):
        self.tstNOK = [
            #Starting value          Starting                        Relative JSON Pointer           result
            #------------------------------------------------------------------------------------------------------
            (self.refx,              "",                            "0#",                            None,),
        ]
        dbgcnt = 0
        for tst in self.tstNOK:
            try:
                startrel = JSONPointer(tst[2], startrel=tst[1])
                #res = startrel.evaluate(self.data)
                res = startrel(self.data)
                self.assertEqual(res, tst[3])
                dbgcnt += 1
            except JSONPointerError as e:
                pass

if __name__ == '__main__':
    unittest.main()
