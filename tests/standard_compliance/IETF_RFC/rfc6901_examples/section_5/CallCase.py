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

"""
from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
else:
    import json as myjson
import jsonschema

from jsondata.jsonpointer import JSONPointer
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF
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
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = self.configdata.data

        assert jdata == jdoc

    def testCase901(self):
        """JSONPointers: "/foo"
        """
        jp = JSONPointer('/foo')
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = [u'bar', u'baz']

        assert jdata == jdoc

    def testCase902(self):
        """JSONPointers: "/foo/0"
        """
        jp = JSONPointer('/foo/0')
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = u'bar'
        # print "<"+repr(jdata)+">"
        # print "<"+jdoc+">"

        assert jdata == jdoc

    def testCase903(self):
        """JSONPointers: "/"
        """
        jp = JSONPointer('/')
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = {'foo': ['bar', 'baz'], '': 0, 'a/b': 1, 'c%d': 2, 'e^f': 3, 'g|h': 4, 'i\\j': 5, 'k"l': 6, ' ': 7, 'm~n': 8}

        assert jdata == jdoc

    def testCase904(self):
        """JSONPointers: "/a~1b"
        """
        jp = JSONPointer('/a~1b', replace=True)
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = 1

        assert jdata == jdoc

    def testCase905(self):
        """JSONPointers: "/c%d"
        """
        jp = JSONPointer('/c%d')
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = 2

        assert jdata == jdoc

    def testCase906(self):
        """JSONPointers: "/e^f"
        """
        jp = JSONPointer('/e^f')
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = 3

        assert jdata == jdoc

    def testCase907(self):
        """JSONPointers: "/g|h"
        """
        jp = JSONPointer('/g|h')
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = 4

        assert jdata == jdoc

    def testCase908(self):
        """JSONPointers: "/i\\j"
        """
        jp = JSONPointer('/i\\j')
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = 5

        assert jdata == jdoc

    def testCase909(self):
        """JSONPointers: "/k\"l"
        """
        jp = JSONPointer('/k\"l')
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = 6

        assert jdata == jdoc

    def testCase910(self):
        """JSONPointers: "/ "
        """
        jp = JSONPointer('/ ')
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = 7

        assert jdata == jdoc
    def testCase911(self):
        """JSONPointers: "/m~0n"
        """
        jp = JSONPointer('/m~0n', replace=True)
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = 8

        assert jdata == jdoc


if __name__ == '__main__':
    unittest.main()
