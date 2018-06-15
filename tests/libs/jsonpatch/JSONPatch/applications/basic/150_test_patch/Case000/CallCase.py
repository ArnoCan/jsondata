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
        self.jsonpatchlist += JSONPatchItem(
            "add", "/a100", "v100")

        self.jsonpatchlist += JSONPatchItem(
            "copy", "/a200", "/a100")

        self.jsonpatchlist += JSONPatchItem(
            "replace", "/a100", 99)

        self.jsonpatchlist += JSONPatchItem(
            "test", "/a100", 99)

        ref = repr(self.jsonpatchlist)
        ref = [{"op": "add", "path": "/a100", "value": "v100"},
               {"op": "copy", "path": "/a200", "from": "/a100"},
               {"op": "replace", "path": "/a100", "value": 99},
               {"op": "test", "path": "/a100", "value": 99}]

        assert ref == self.jsonpatchlist

        n, err = self.jsonpatchlist.apply(configdata)

        ref = {"foo": "bar", "a100": "99", "a200": "v100"}
        assert n == 4
        assert err == []
        assert sorted(ref) == sorted(configdata.get_data())


if __name__ == '__main__':
    unittest.main()
