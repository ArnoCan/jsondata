# -*- coding: utf-8 -*-
"""Standards tests from RFC6901 for compliance of pointer syntax.

This case covers in particular the standard contained examples.
For JSON notation of RFC6901::

  ""           // the whole document
  "/foo"       ["bar", "baz"]
  "/foo/0"     "bar"
  "/"          0
  "/a~1b"      1
  "/c%d"       2
  "/e^f"       3
  "/g|h"       4
  "/i\\j"      5
  "/k\"l"      6
  "/ "         7
  "/m~0n"      8

For fragments notation of RFC6901/RFC3986::

  #            // the whole document            
  #/foo        ["bar", "baz"]
  #/foo/0      "bar"
  #/           0
  #/a~1b       1
  #/c%25d      2
  #/e%5Ef      3
  #/g%7Ch      4
  #/i%5Cj      5
  #/k%22l      6
  #/%20        7
  #/m~0n       8

"""
from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson
else:
    import json as myjson
import jsonschema

from jsondata.jsonpointer import JSONPointer
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF
from jsondata.jsonpatch import JSONPatch, JSONPatchItem, JSONPatchItemRaw
from jsondata.jsonpointer import JSONPointer
from filesysobjects.configdata import ConfigPath


class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        _cp = ConfigPath(replace=os.path.dirname(__file__))
        self.datafile = _cp.get_config_filepath('rfc6901.json')
        self.configdata = ConfigData(
            {},
            datafile=self.datafile,
            validator=MS_OFF,
            )

    def testCase900(self):
        """JSONPointers: ""
        """
        jp = JSONPointer('')
        jdata = jp(self.configdata.data)
        jdoc = {u'': 0, u' ': 7, u'c%d': 2, u'a/b': 1, u'k"l': 6, u'm~n': 8, u'g|h': 4, u'e^f': 3, u'foo': [u'bar', u'baz'], u'i\\j': 5}

        assert jdata == jdoc

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


#
#######################
#
if __name__ == '__main__':
    unittest.main()
