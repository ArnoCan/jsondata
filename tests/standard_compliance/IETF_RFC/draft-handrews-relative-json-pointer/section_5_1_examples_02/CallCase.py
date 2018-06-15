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

Starting from the value {"objects":true} (corresponding to the member
key "nested"), the following JSON strings evaluate to the
accompanying values:

   "0/objects"            true
   "1/nested/objects"     true
   "2/foo/0"              "bar"
   "0#"                   "nested"
   "1#"                   "highly"

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

        self.tstOK = [
            #Starting value          Starting                        Relative JSON Pointer           result
            #------------------------------------------------------------------------------------------------------
            ({"objects":True},       "/highly/nested",               "0/objects",                    True,),  # true
            ({"objects":True},       "/highly/nested",               "1/nested/objects",             True,),  # true
            ({"objects":True},       "/highly/nested",               "2/foo/0",                      "bar",),
            ({"objects":True},       "/highly/nested",               "0#",                           "nested",),
            ({"objects":True},       "/highly/nested",               "1#",                           "highly",),
        ]

#     def testCase010(self):
# #        startrel = JSONPointer('0#', startrel=startrel)
# 
# 
#         #startrel = JSONPointer("/test/1")
#         
#         # define the pointer
#         relpointer = JSONPointerWithRel('0#')
#         
#         # FIXME:
#         s0 = str(relpointer)
# 
#         self.assertEqual(relpointer , '0#')
# 
#         # define the start node as offset
#         startnode = JSONPointer("/test/1")(self.data)
#         self.assertEqual(startnode, 'bar')
# 
#         # get the resulting node
#         res0 = relpointer(self.data)
#         res0 = relpointer(self.data)(startnode)
#         res0 = relpointer.set_top(self.data)(startnode)
# 
#         # same for short
#         res1 = JSONPointer('0#')(JSONPointer("/test/1")(self.data))
# 
#         
#         resx = "bar"
#         self.assertEqual(res0, res1)
#         self.assertEqual(res0, resx)

    def testCase100(self):
        for tst in self.tstOK:
            try:
                startrel = JSONPointer(tst[2], startrel=tst[1])
                res = startrel(self.data)
                self.assertEqual(res, tst[3])
            except Exception as e:
                raise Exception(
                    str(e)
                    + "\n" + str(tst)
                    )  # from None


if __name__ == '__main__':
    unittest.main()
