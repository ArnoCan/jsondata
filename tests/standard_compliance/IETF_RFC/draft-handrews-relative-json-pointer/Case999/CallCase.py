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
    import ujson as myjson
else:
    import json as myjson
import jsonschema


jval = None

from jsondata import JSONPointerError
from jsondata.jsonpointer import JSONData
from jsondata.jsonpointer import JSONPointer
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF
from filesysobjects.configdata import ConfigPath


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

        p = JSONPointer('0#', startrel=JSONPointer('/test/1'))

        s0 = str(p)
        r0 = repr(p)

        d = p(self.data)

        _cp = ConfigPath(replace=os.path.dirname(__file__))
        self.datafile = _cp.get_config_filepath('rfc6901.json')
        self.configdata = ConfigData(
            {},
            datafile=self.datafile,
            validator=MS_OFF,
            )

    def testCase000(self):
        startrel = JSONPointer('/')
        try:
            res = startrel(self.data)
        except (JSONPointerError, KeyError):
            pass
        else:
            raise JSONPointerError()

    def testCase001(self):
        startrel = JSONPointer('//')
        try:
            res = startrel(self.data)
        except JSONPointerError:
            pass
        else:
            raise JSONPointerError()

    def testCase010(self):
        startrel=JSONPointer('/test/1')
        res = startrel(self.data)
        self.assertEqual(res, "bar")

    def testCase900(self):
        """JSONPointers: ""
        """
        jp = JSONPointer('')
        jdata = jp(self.configdata.data)
        jdoc = {u'': 0, u' ': 7, u'c%d': 2, u'a/b': 1, u'k"l': 6, u'm~n': 8, u'g|h': 4, u'e^f': 3, u'foo': [u'bar', u'baz'], u'i\\j': 5}
#         print("<"+repr(jdata)+">")
#         print("<"+repr(jdoc)+">")

        assert jdata == jdoc
        pass

    def testCase901(self):
        """JSONPointers: "/foo"
        """
        jp = JSONPointer('/foo')
        jdata = jp(self.configdata.data)
        jdoc = [u'bar', u'baz']

        assert jdata == jdoc

    def testCase902(self):
        """JSONPointers: "/foo/0"
        """
        jp = JSONPointer('/foo/0')
        jdata = jp(self.configdata.data)
        jdoc = u'bar'

        assert jdata == jdoc

    def testCase903(self):
        """JSONPointers: "/"
        """
        jp = JSONPointer('/')
        jdata = jp(self.configdata.data)
        jdoc = 0

        assert jdata == jdoc

    def testCase904(self):
        """JSONPointers: "/a~1b"
        """
        jp = JSONPointer('/a~1b', replace=True)
        jdata = jp(self.configdata.data)
        jdoc = 1

        assert jdata == jdoc

    def testCase905(self):
        """JSONPointers: "/c%d"
        """
        jp = JSONPointer('/c%d')
        jdata = jp(self.configdata.data)
        jdoc = 2

        assert jdata == jdoc

    def testCase906(self):
        """JSONPointers: "/e^f"
        """
        jp = JSONPointer('/e^f')
        jdata = jp(self.configdata.data)
        jdoc = 3

        assert jdata == jdoc

    def testCase907(self):
        """JSONPointers: "/g|h"
        """
        jp = JSONPointer('/g|h')
        jdata = jp(self.configdata.data)
        jdoc = 4

        assert jdata == jdoc

    def testCase908(self):
        """JSONPointers: "/m~0n"
        """
        jp = JSONPointer('/m~0n', replace=True)
        jdata = jp(self.configdata.data)
        jdoc = 8

        assert jdata == jdoc


if __name__ == '__main__':
    unittest.main()
