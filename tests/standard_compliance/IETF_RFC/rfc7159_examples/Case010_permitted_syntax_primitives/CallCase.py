# -*- coding: utf-8 -*-
"""Standards tests from RFC7159, Chapter 13, Example 2
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
from jsondata.jsonpatch import JSONPatch, JSONPatchItem, JSONPatchItemRaw
from jsondata.jsonpointer import JSONPointer
from filesysobjects.configdata import ConfigPath


class CallUnits(unittest.TestCase):

    def testCase010_float(self):

        _cp = ConfigPath(replace=os.path.dirname(__file__))
        datafile = _cp.get_config_filepath('rfc7159_error_primitive_int.json')
        configdata = ConfigData(
            None,
            datafile=datafile,
            validator=MS_OFF,
            )

        jdoc = 99

        assert configdata.data == 99
        assert configdata.data == jdoc

    def testCase020_float(self):
        """Verify: rfc7159: syntax error primitive: float
        """
        _cp = ConfigPath(replace=os.path.dirname(__file__))
        datafile = _cp.get_config_filepath('rfc7159_error_primitive_float.json')
        configdata = ConfigData(
            None,
            datafile=datafile,
            validator=MS_OFF,
            )

        jdoc = -122.3959

        assert configdata.data == -122.3959
        assert configdata.data == jdoc

    def testCase020_bool(self):
        """Verify: rfc7159: syntax error primitive: boolean
        """
        _cp = ConfigPath(replace=os.path.dirname(__file__))
        datafile = _cp.get_config_filepath('rfc7159_error_primitive_boolean.json')
        configdata = ConfigData(
            None,
            datafile=datafile,
            validator=MS_OFF,
            )

        jdoc = True

        assert configdata.data == True
        assert configdata.data == jdoc


if __name__ == '__main__':
    unittest.main()

            
