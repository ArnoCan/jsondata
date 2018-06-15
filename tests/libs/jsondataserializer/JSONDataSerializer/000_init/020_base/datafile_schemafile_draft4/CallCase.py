from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport @UnusedImport pylint: disable=import-error
else:
    import json as myjson  # @Reimport
import jsonschema  # @UnusedImport


from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata import MS_DRAFT4


class CallUnits(unittest.TestCase):

    def testCase100(self):
        unittest.TestCase.setUp(self)

        # datafile
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('datafile.json')
        if not os.path.isfile(datafile):
            raise BaseException("Missing JSON data:file=" + str(datafile))

        with open(datafile) as data_file:
            jval_raw = myjson.load(data_file)
        if jval_raw == None:
            raise BaseException("Failed to load data:" + str(data_file))


        # schema
        schemafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('schema.jsd')
        if not os.path.isfile(schemafile):
            raise BaseException("Missing JSONschema:file=" + str(schemafile))
        with open(schemafile) as schema_file:
            sval = myjson.load(schema_file)
        if sval == None:
            raise BaseException("Failed to load schema:" + str(schema_file))

        jval = {}
        configdata = ConfigData(
            jval,
            datafile=datafile,
            schemafile=schemafile,
            validator= MS_DRAFT4,
            )

        self.assertEqual(jval, jval_raw)
        self.assertEqual(configdata, jval_raw)

        assert configdata.data["address"]["streetAddress"] == "21 2nd Street"
        assert configdata.data["address"]["city"] == "New York"
        assert configdata.data["address"]["houseNumber"] == 12

        assert configdata.data["phoneNumber"][0]["type"] == "home"
        assert configdata.data["phoneNumber"][0]["number"] == "212 555-1234"

        assert configdata.data["address"]["streetAddress"] == jval["address"]["streetAddress"]
        assert configdata.data["address"]["city"] == jval["address"]["city"]
        assert configdata.data["address"]["houseNumber"] == jval["address"]["houseNumber"]

        assert configdata.data["phoneNumber"][0]["type"] == jval["phoneNumber"][0]["type"]
        assert configdata.data["phoneNumber"][0]["number"] == jval["phoneNumber"][0]["number"]


if __name__ == '__main__':
    unittest.main()

