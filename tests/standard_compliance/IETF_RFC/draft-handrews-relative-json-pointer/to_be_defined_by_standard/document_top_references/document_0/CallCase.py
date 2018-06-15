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
            "": 2,
            "a": [3, 4]
        }

        self.data = JSONData(self.refx)

    def testCase100(self):
        dbgcnt = 0
        self.tstOK = [
            #Starting value          Starting                        Relative JSON Pointer           result
            #------------------------------------------------------------------------------------------------------
            (self.refx,              "",                            "0",                             self.refx,),
            (self.refx[""],          "/",                           "0#",                            "",),
            (self.refx[""],          "",                            "0/",                            2,),
            (self.refx[""],          "/",                           "0",                             2,),
        ]
        for tst in self.tstOK:
            try:
                startrel = JSONPointer(tst[2], startrel=tst[1])
                # res = startrel.evaluate(self.data)
                res = startrel(self.data)
                self.assertEqual(res, tst[3])
                dbgcnt += 1
            except Exception as e:
                raise Exception(
                    str(e)
                    + "\n" + str(tst)
                    )  # from None

    def testCase200(self):
        dbgcnt = 0
        self.tstNOK = [
            #Starting value          Starting                        Relative JSON Pointer           result
            #------------------------------------------------------------------------------------------------------
            (self.refx,              "",                            "0#",                            None,),
            (self.refx,              "",                            "0",                             self.refx,),
            (self.refx[""],          "/",                           "0#",                            "",),
            (self.refx[""],          "",                            "0/",                            2,),
            (self.refx[""],          "/",                           "0",                             2,),
        ]
        for tst in self.tstNOK:
            try:
                startrel = JSONPointer(tst[2], startrel=tst[1])
                # res = startrel.evaluate(self.data)
                res = startrel(self.data)
                self.assertEqual(res, tst[3])
                dbgcnt += 1
            except JSONPointerError:
                pass
#             except Exception as e:
#                 raise Exception(
#                     str(e)
#                     + "\n" + str(tst)
#                     )  # from None

if __name__ == '__main__':
    unittest.main()
