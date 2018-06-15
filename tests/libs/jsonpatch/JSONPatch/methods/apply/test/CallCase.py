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

        jsonpatchlist = JSONPatch()
        jsonpatchlist += JSONPatchItem("add", "/ax", "v100")
        jsonpatchlist += JSONPatchItem("add", "/bx", 100)
        jsonpatchlist += JSONPatchItem("copy", "/axcopy", "/ax")
        jsonpatchlist += JSONPatchItem("copy", "/bxcopy", "/bx")
        jsonpatchlist += JSONPatchItem("replace", "/ax", "new")
        jsonpatchlist += JSONPatchItem("replace", "/bx", 8)

        ref = [{"op": "add", "path": "/ax", "value": "v100"},
               {"op": "add", "path": "/bx", "value": 100},
               {"op": "copy", "path": "/axcopy", "from": "/ax"},
               {"op": "copy", "path": "/bxcopy", "from": "/bx"},
               {"op": "replace", "path": "/ax", "value": "new"},
               {"op": "replace", "path": "/bx", "value": 8},
               ]
        assert ref == jsonpatchlist

        n, err = jsonpatchlist.apply(configdata)
        # print repr(configdata)
        ref = sorted( 
                     {
                         "foo": "bar",
                         "ax": "new",
                         "bx": 8,
                         "axcopy": "v100",
                         "bxcopy": 100,
                         }
                     )

        assert n == 6
        assert err == []
        assert sorted(ref) == sorted(configdata.get_data())
        newconf = configdata

        jsonpatchlist = JSONPatch()
        jsonpatchlist += JSONPatchItem("test", "/ax", "new")
        jsonpatchlist += JSONPatchItem("test", "/bx", 8)
        jsonpatchlist += JSONPatchItem("test", "/axcopy", "v100")
        jsonpatchlist += JSONPatchItem("test", "/bxcopy", 100)

        n, err = jsonpatchlist.apply(newconf)

        assert n == 4
        assert err == []

        ref = {
            "foo": "bar",
            "ax": "new",
            "bx": 8,
            "axcopy": "v100",
            "bxcopy": 100,
            }
        assert sorted(ref) == sorted(newconf)


if __name__ == '__main__':
    unittest.main()
