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


jval = None
configdata = None

from jsondata import MJ_RFC4627, JSONDataModeError
from jsondata.jsonpointer import JSONPointer
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata.jsondata import MS_OFF, JSONDataNodeTypeError
from filesysobjects.configdata import ConfigPath


class CallUnits(unittest.TestCase):

    def testCase010_int(self):
        """Verify: rfc4627: syntax error primitive: integer
        """
        
        try:
            _cp = ConfigPath(replace=os.path.dirname(__file__))
            datafile = _cp.get_config_filepath('rfc4627_error_primitive_int.json')
            configdata = ConfigData(
                None,
                datafile=datafile,
                validator=MS_OFF,
                mode=MJ_RFC4627,
                )
        except JSONDataModeError:
            pass
        else:
            raise JSONDataNodeTypeError("primitives as documents are prohibited in RFC4627")

    def testCase020_float(self):
        """Verify: rfc4627: syntax error primitive: float
        """
        try:
            _cp = ConfigPath(replace=os.path.dirname(__file__))
            datafile = _cp.get_config_filepath('rfc4627_error_primitive_float.json')
            configdata = ConfigData(
                None,
                datafile=datafile,
                validator=MS_OFF,
                mode=MJ_RFC4627,
                )

        except JSONDataModeError:
            pass
        else:
            raise JSONDataNodeTypeError("primitives as documents are prohibited in RFC4627")

    def testCase020_bool(self):
        """Verify: rfc4627: syntax error primitive: boolean
        """

        try:
            _cp = ConfigPath(replace=os.path.dirname(__file__))
            datafile = _cp.get_config_filepath('rfc4627_error_primitive_boolean.json')
            configdata = ConfigData(
                None,
                datafile=datafile,
                validator=MS_OFF,
                mode=MJ_RFC4627,
                )
        except JSONDataModeError:
            pass
        else:
            raise JSONDataNodeTypeError("primitives as documents are prohibited in RFC4627")

if __name__ == '__main__':
    unittest.main()
