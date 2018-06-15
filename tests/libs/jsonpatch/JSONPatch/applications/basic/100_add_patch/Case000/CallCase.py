# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import unittest
import os
import sys

from jsondata import V3K

if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport pylint: disable=import-error
else:
    import json as myjson
import jsonschema

if V3K:
    unicode = str


from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF
from jsondata.jsonpatch import JSONPatch, JSONPatchItem
from filesysobjects.configdata import ConfigPath


class CallUnits(unittest.TestCase):

    def testCase004(self):

        _cp = ConfigPath(replace=os.path.dirname(__file__))
        datafile = _cp.get_config_filepath('data.json')
        schemafile = _cp.get_config_filepath('schema.jsd')
        configdata = ConfigData(
            {},
            datafile=datafile,
            schemafile=schemafile,
            validator=MS_OFF,
            )

        self.jsonpatchlist = JSONPatch()
        for i in range(0, 10):
            self.jsonpatchlist += JSONPatchItem(
                "add", "/a" + unicode(i), "v" + unicode(i))

        ref = [{u'op': u'add', u'path': u'/a0', u'value': u'v0'}, {u'op': u'add', u'path': u'/a1', u'value': u'v1'}, {u'op': u'add', u'path': u'/a2', u'value': u'v2'}, {u'op': u'add', u'path': u'/a3', u'value': u'v3'}, {u'op': u'add', u'path': u'/a4', u'value': u'v4'}, {u'op': u'add', u'path': u'/a5', u'value': u'v5'}, {u'op': u'add', u'path': u'/a6', u'value': u'v6'}, {u'op': u'add', u'path': u'/a7', u'value': u'v7'}, {u'op': u'add', u'path': u'/a8', u'value': u'v8'}, {u'op': u'add', u'path': u'/a9', u'value': u'v9'}]

        assert ref == self.jsonpatchlist

        self.jsonpatchlist = JSONPatch()
        self.jsonpatchlist += JSONPatchItem(
            "add", "/b", 11)

        ref = [{u'op': u'add', u'path': u'/b', u'value': 11}]

        assert ref == self.jsonpatchlist


if __name__ == '__main__':
    unittest.main()
