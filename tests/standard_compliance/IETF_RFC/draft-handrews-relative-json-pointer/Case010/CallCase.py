# -*- coding: utf-8 -*-
"""Standards tests from the IETF draft for relative pointer.

See: https://gist.github.com/geraintluff
https://gist.github.com/geraintluff/5911303

This case covers in particular the standard contained examples. ::

{
    "test": ["foo", "bar"],
    "child": {
        "grandchild": 12345
    },
    "sibling": "sibling value",
    "awkwardly/named~variable": true
}

For JSON notation of RFC6901::

 Starting value         Relative JSON Pointer           result
-------------------------------------------------------------------------
"bar"                   "0"                             "bar"
"bar"                   "0#"                            1
"bar"                   "1"                             ["foo", "bar"]
"bar"                   "1/0"                           "foo"
"bar"                   "1/1"                           "bar"
"bar"                   "1#"                            "test"
"bar"                   "2"                             << the whole document >>
"bar"                   "2#"                            << fails >>
"bar"                   "3"                             << fails >>
12345                   "0"                             12345
12345                   "0#"                            "grandchild"
12345                   "1"                             {"grandchild": 12345}
12345                   "1/grandchild"                  12345
12345                   "1#"                            "child"
12345                   "2"                             << the whole document >>
12345                   "2/sibling"                     "sibling value"
12345                   "2/test/1"                      "bar"
{"grandchild": 12345}   "0"                             {"grandchild": 12345}
{"grandchild": 12345}   "0#"                            "child"
{"grandchild": 12345}   "0/grandchild"                  12345
{"grandchild": 12345}   "1/sibling"                     "sibling value"
{"grandchild": 12345}   "2"                             << the whole document >>
"sibling value"         "0"                             "sibling value"
"sibling value"         "0#"                            "sibling"
"sibling value"         "1"                             << the whole document >>
"sibling value"         "1/awkwardly~1named~0variable"  true
true                    "0"                             true
true                    "0#"                            "awkwardly/named-variable"
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
from jsondata  import MS_OFF, JSONPointerError

# name of application, used for several filenames as MS_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME


class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        
        self.refx = {
            "test": ["foo", "bar"],
            "child": {
                "grandchild": 12345
            },
            "sibling": "sibling value",
            "awkwardly/named~variable": True # true
        }

        self.data = JSONData(self.refx)

        self.tstOK = [
            #Starting value          Starting                        Relative JSON Pointer           result
            #------------------------------------------------------------------------------------------------------
            #ERROR: ("bar",                  "/test/1",                     "0",                            "bar",),
            ("bar",                  "/test/1",                     "0#",                            1,),
            ("bar",                  "/test/1",                     "1",                            ["foo", "bar"],),
            ("bar",                  "/test/1",                     "1/0",                           "foo",),
            ("bar",                  "/test/1",                     "1/1",                           "bar",),
            ("bar",                  "/test/1",                     "1#",                            "test",),
            ("bar",                  "/test/1",                     "2",                            self.data,),
            (12345,                  "/child/grandchild",           "0",                            12345,),
            (12345,                  "/child/grandchild",           "0#",                            "grandchild",),
            (12345,                  "/child/grandchild",           "1",                            {"grandchild": 12345},),
            (12345,                  "/child/grandchild",           "1/grandchild",                  12345,),
            (12345,                  "/child/grandchild",           "1#",                            "child",),
            (12345,                  "/child/grandchild",           "2",                             self.data,),
            (12345,                  "/child/grandchild",           "2/sibling",                     "sibling value",),
            (12345,                  "/child/grandchild",           "2/test/1",                      "bar",),
            ({"grandchild": 12345},  "/child",                      "0",                             {"grandchild": 12345},),
            ({"grandchild": 12345},  "/child",                      "0#",                            "child",),
            ({"grandchild": 12345},  "/child",                      "0/grandchild",                  12345,),
            ({"grandchild": 12345},  "/child",                      "1/sibling",                     "sibling value",),
            ({"grandchild": 12345},  "/child",                      "2",                             self.data,),
            ("sibling value",        "/sibling",                    "0",                             "sibling value",),
            ("sibling value",        "/sibling",                    "0#",                            "sibling",),
            ("sibling value",        "/sibling",                    "1",                             self.data,),
            ("sibling value",        "/sibling",                    "1/awkwardly~1named~0variable",   True,),
            (True,                   "/awkwardly~1named~0variable",  "0",                            True,),
#            (True,                   "0#",                            "awkwardly/named-variable",),
        ]


        self.tstNOK = [
            #Starting value         Relative JSON Pointer           result
            #-------------------------------------------------------------------------
            ("bar",                  "2#",                            False,), #<< fails >>
            ("bar",                  "3",                             False,), #<< fails >>
        ]

    def testCase100(self):
        dbgcnt = 0
        for tst in self.tstOK:
            try:
                startrel = JSONPointer(tst[2], startrel=tst[1])
                res = startrel(self.data)
                self.assertEqual(res, tst[3])
                dbgcnt += 1
            except JSONPointerError:
                pass
            except Exception as e:
                raise Exception(
                    str(e)
                    + "\n" + str(tst)
                    )  # from None


if __name__ == '__main__':
    unittest.main()
