"""Load and access data.
"""
from __future__ import absolute_import

import os
import sys
import unittest
import copy


if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
else:
    import json as myjson  # @Reimport
import jsonschema  # @UnusedImport


jval = None

from jsondata.jsondataserializer import JSONDataSerializer as JSONDataLoader
from jsondata  import MS_OFF
from jsondata.jsondata import JSONData, C_DEEP, C_REF, C_SHALLOW


class CallUnits(unittest.TestCase):

    def testCase010(self):
        unittest.TestCase.setUp(self)

        data = JSONData(
            [u'a', u'b', u'c'],
            )

        resx = [u'a', u'b', u'c']

        assert data == resx

        res = []
        with data as dat:
            for d in dat:
                res.append(d)
        
        assert res == resx
        
        
    def testCase020(self):
        unittest.TestCase.setUp(self)

        data = JSONData(
            [u'a', u'b', u'c'],
            )

        resx = [u'a', u'b', u'c']

        assert data == resx

        resx = {0: u'a', 1: u'b', 2: u'c'}
        res = {}
        with data as dat:
            for i,v in dat.get_data_items():
                res[i] = v
        
        assert res == resx
        

if __name__ == '__main__':
    unittest.main()
