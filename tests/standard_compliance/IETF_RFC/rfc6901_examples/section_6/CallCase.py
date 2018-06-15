# -*- coding: utf-8 -*-
"""Standards tests from RFC6901 for compliance of pointer syntax.

This case covers in particular the standard contained examples.
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
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
else:
    import json as myjson
import jsonschema

from jsondata import MS_OFF
from jsondata.jsonpointer import JSONPointer
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
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
        """JSONPointers: "#"
        """
        uri_fragment = '#'
        jp = JSONPointer(uri_fragment)
        
        jdata = jp.get_node_value(self.configdata.data)
        jdoc = {u'': 0, u' ': 7, u'c%d': 2, u'a/b': 1, u'k"l': 6, u'm~n': 8, u'g|h': 4, u'e^f': 3, u'foo': [u'bar', u'baz'], u'i\\j': 5}

        assert jdata == jdoc

    def testCase901(self):
        """JSONPointers: "#/foo"
        """
        uri_fragment = '#/foo'
        jp = JSONPointer(uri_fragment)

        jdata = jp.get_node_value(self.configdata.data)
        jdoc = [u'bar', u'baz']

        assert jdata == jdoc

    def testCase902(self):
        """JSONPointers: "#/foo/0"
        """
        uri_fragment = '#/foo/0'
        jp = JSONPointer(uri_fragment)

        jdata = jp.get_node_value(self.configdata.data)
        jdoc = u'bar'

        assert jdata == jdoc

    def testCase903(self):
        """JSONPointers: "#/"
        """
        uri_fragment = '#/'
        jp = JSONPointer(uri_fragment)

        jdata = jp.get_node_value(self.configdata.data)
        jdoc = self.configdata.data

        assert jdata == jdoc

    def testCase904(self):
        """JSONPointers: "#/a~1b"
        """
        uri_fragment = '#/a~1b'
        jp = JSONPointer(uri_fragment, replace=True)

        jdata = jp.get_node_value(self.configdata.data)
        jdoc = 1

        assert jdata == jdoc

    def testCase905(self):
        """JSONPointers: "#/c%25d"
        """
        uri_fragment = '#/c%25d'
        jp = JSONPointer(uri_fragment)

        jdata = jp.get_node_value(self.configdata.data)
        jdoc = 2

        assert jdata == jdoc

    def testCase906(self):
        """JSONPointers: "#/e%5Ef"
        """
        uri_fragment = '#/e%5Ef'
        jp = JSONPointer(uri_fragment)

        jdata = jp.get_node_value(self.configdata.data)
        jdoc = 3

        assert jdata == jdoc

    def testCase907(self):
        """JSONPointers: "#/g%7Ch"
        """
        uri_fragment = '#/g%7Ch'
        jp = JSONPointer(uri_fragment)

        jdata = jp.get_node_value(self.configdata.data)
        jdoc = 4

        assert jdata == jdoc

    def testCase908(self):
        """JSONPointers: "#/m~0n"
        """
        uri_fragment = '#/m~0n'
        jp = JSONPointer(uri_fragment, replace=True)

        jdata = jp.get_node_value(self.configdata.data)
        jdoc = 8

        assert jdata == jdoc

    def testCase909(self):
        """JSONPointers: "#/i%5Cj"
        """
        uri_fragment = '#/i%5Cj'
        jp = JSONPointer(uri_fragment)

        jdata = jp.get_node_value(self.configdata.data)
        jdoc = """5"""

        assert repr(jdata) == jdoc

    def testCase910(self):
        """JSONPointers: "#/k%22l"
        """
        uri_fragment = '#/k%22l'
        jp = JSONPointer(uri_fragment)

        jdata = jp.get_node_value(self.configdata.data)
        jdoc = """6"""

        assert repr(jdata) == jdoc

    def testCase911(self):
        """JSONPointers: "#/%20"
        """
        uri_fragment = '#/%20'
        jp = JSONPointer(uri_fragment)

        jdata = jp.get_node_value(self.configdata.data)
        jdoc = """7"""

        assert repr(jdata) == jdoc


#
#######################
#
if __name__ == '__main__':
    unittest.main()
