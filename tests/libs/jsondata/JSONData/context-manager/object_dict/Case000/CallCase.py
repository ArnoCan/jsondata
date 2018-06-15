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
            {u'a': 10, u'b': 11, u'c': 12},
            )

        resx = {u'a': 10, u'b': 11, u'c': 12}

        assert data == resx

        res = {}
        for k,v in data.get_data_items():
            res[k] = v
        
        assert res == resx
        
    def testCase020(self):
        unittest.TestCase.setUp(self)

        data = JSONData(
            {u'a': 10, u'b': 11, u'c': 12},
            )

        resx = {u'a': 10, u'b': 11, u'c': 12}

        assert data == resx

        res = {}
        for k in data:
            res[k] = data[k]
        
        assert res == resx

if __name__ == '__main__':
    unittest.main()
