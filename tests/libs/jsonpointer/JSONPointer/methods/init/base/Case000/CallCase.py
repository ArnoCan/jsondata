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
from jsondata.jsonpointer import JSONPointer


class CallUnits(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
 
        _cp = ConfigPath(replace=os.path.dirname(__file__))
        datafile = _cp.get_config_filepath('testdata.json')
        schemafile = _cp.get_config_filepath('testdata.jsd')
        self.configdata = ConfigData(
            {},
            datafile=datafile,
            schemafile=schemafile,
            validator=MS_OFF,
            )

        # data
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('testdata.json')
        if not os.path.isfile(datafile):
            raise BaseException("Missing JSON data:file=" + str(datafile))
        # load data
        with open(datafile) as data_file:
            self.jval = myjson.load(data_file)
        if self.jval == None:
            raise BaseException("Failed to load data:" + str(data_file))

        assert self.jval

    def testCase900(self):

        assert self.configdata.data["address"]["streetAddress"] == "21 2nd Street"
        assert self.configdata.data["address"]["city"] == "New York"
        assert self.configdata.data["address"]["houseNumber"] == 12

    def testCase901(self):

        assert self.configdata.data["phoneNumber"][0]["type"] == "home0"
        assert self.configdata.data["phoneNumber"][0]["number"] == "000"
        pass

    def testCase920(self):

        assert self.configdata.data["address"]["streetAddress"] == self.jval["address"]["streetAddress"]
        assert self.configdata.data["address"]["city"] == self.jval["address"]["city"]
        assert self.configdata.data["address"]["houseNumber"] == self.jval["address"]["houseNumber"]

    def testCase921(self):

        assert self.configdata.data["phoneNumber"][0]["type"] == self.jval["phoneNumber"][0]["type"]
        assert self.configdata.data["phoneNumber"][0]["number"] == self.jval["phoneNumber"][0]["number"]
        pass

    def testCase922(self):

        # print "#---------------a"
        for l in ['domestic', 'abroad', ]:
            for n in [0, 1, ]:
                cdata = self.configdata.data["customers"][l][n]["name"]
                jdata = self.jval["customers"][l][n]["name"]
                assert cdata == jdata

                cdata = self.configdata.data["customers"][l][n]["industries"]
                jdata = self.configdata.data["customers"][l][n]["industries"]
                assert cdata == jdata

                for p in [0, 1, ]:
                    cdata = self.configdata.data["customers"][l][n]["products"][p]["name"]
                    jdata = self.configdata.data["customers"][l][n]["products"][p]["name"]
                    assert cdata == jdata

                    cdata = self.configdata.data["customers"][l][n]["products"][p]["quantities"]
                    jdata = self.configdata.data["customers"][l][n]["products"][p]["quantities"]
                    assert cdata == jdata

                    cdata = self.configdata.data["customers"][l][n]["products"][p]["priority"]
                    jdata = self.configdata.data["customers"][l][n]["products"][p]["priority"]
                    assert cdata == jdata


if __name__ == '__main__':
    unittest.main()
