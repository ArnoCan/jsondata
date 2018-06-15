# -*- coding: utf-8 -*-
"""Standards tests from the IETF draft for relative pointer.

See: https://gist.github.com/geraintluff

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
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
else:
    import json as myjson
import jsonschema


jval = None

from jsondata import JSONPointerError, JSONDataParameterError
from jsondata.jsonpointer import JSONData
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
            "test": ["foo", "bar"],
            "child": {
                "grandchild": 12345
            },
            "sibling": "sibling value",
            "awkwardly/named~variable": True # true
        }

        self.data = JSONData(self.refx)

    def testCase000(self):
        """
         Starting value         Relative JSON Pointer           result
        -------------------------------------------------------------------------
        ""                      "0#"                            << fails >>
        """
        try:
            startrel = JSONPointer('0#', startrel='')  # @UnusedVariable
        except JSONPointerError:
            pass

    def testCase010(self):
        """
         Starting value         Relative JSON Pointer           result
        -------------------------------------------------------------------------
        "/"                     "0#"                            null/None
        """
        startrel = JSONPointer('0#', startrel='/')

        res = startrel.get_key()

        resx = None
        self.assertEqual(res, resx)

    def testCase020(self):
        """
         Starting value         Relative JSON Pointer           result
        -------------------------------------------------------------------------
        "/"                     "0"                             << fails >>
        """
        startrel = JSONPointer('0', startrel='/')
        
        # pointer - data
        k = startrel.get_key()
        kx = ''
        self.assertEqual(k, kx)

        # document data
        try:
            res = startrel(self.data)  # @UnusedVariable
        except JSONPointerError:
            pass

    def testCase30(self):
        """
         Starting value         Relative JSON Pointer           result
        -------------------------------------------------------------------------
        ""                      "0/"                            << fails >>
        """
        startrel = JSONPointer('0/', startrel='')

        # pointer - data
        k = startrel.get_key()
        kx = ''
        self.assertEqual(k, kx)

        # document data
        try:
            res = startrel(self.data)  # @UnusedVariable
        except JSONPointerError:
            pass


if __name__ == '__main__':
    unittest.main()
