# -*- coding: utf-8 -*-
"""Standards tests from the IETF draft for relative pointer.

5.1. Examples
For example, given the JSON document:

   {
      "foo": ["bar", "baz"],
    "highly": {
       "nested": {
          "objects": true
       }
   }
}

Starting from the value "baz" (inside "foo"), the following JSON
strings evaluate to the accompanying values:

   "0"                           "baz"
   "1/0"                         "bar"
   "2/highly/nested/objects"     true
   "0#"                          1
   "1#"                          "foo"

"""
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

from jsondata import V3K
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
            "foo": ["bar", "baz"],
            "highly": {
               "nested": {
                  "objects": True  # true
               }
           }
        }

        self.data = JSONData(self.refx)


    def testCase100(self):
        self.tstOK = [
            #Starting value          Starting                        Relative JSON Pointer           result
            #------------------------------------------------------------------------------------------------------
            ("baz",                  "/foo/1",                      "0",                             "baz",),
            ("baz",                  "/foo/1",                      "1/0",                           "bar",),
            ("baz",                  "/foo/1",                      "2/highly/nested/objects",       True,), # true
            ("baz",                  "/foo/1",                      "0#",                            1,),
            ("baz",                  "/foo/1",                      "1#",                            "foo",),
        ]
        debug_cnter = 0
        for tst in self.tstOK:
            #
#             print("\n*** 4TEST:idx=" + str(debug_cnter))
            try:
                relpointer = JSONPointer(tst[2], startrel=tst[1])
                
                s0 = str(relpointer)
                r0 = repr(relpointer)
                
                res = relpointer(self.data)
                self.assertEqual(res, tst[3])

                # res = relpointer(self.data)

                debug_cnter += 1

            except Exception as e:
                if V3K:
                    raise Exception(
                        str(e)
                        + "\ntest-record[" + str(debug_cnter) + "]=" + str(tst)
                        )  # here for tests we want the pure nested
                else:
                    raise Exception(
                        str(e)
                        + "\n" + str(tst)
                        )


if __name__ == '__main__':
    unittest.main()
