"""Check internal generator loops.
"""
from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson  # @UnresolvedImport  @UnusedImport pylint: disable=import-error
else:
    import json as myjson  # @Reimport
import jsonschema  # @UnusedImport

from filesysobjects.configdata import ConfigPath
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF


class CallUnits(unittest.TestCase):

    def testCase000(self):
        # data
        datafile = os.path.abspath(os.path.dirname(
            __file__)) + os.sep + str('testdata.json')
        if not os.path.isfile(datafile):
            raise BaseException("Missing JSON data:file=" + str(datafile))

        # load data
        with open(datafile) as data_file:
            jval = myjson.load(data_file)
        if jval == None:
            raise BaseException("Failed to load data:" + str(data_file))



        _sp = [
            os.path.dirname(__file__),
            "$HOME/etc/",
            "~/etc/",
            "$PWD/tmp/",
            os.path.dirname(__file__) + os.sep + 'testsubdir0' + os.sep,
            os.path.dirname(__file__) + os.sep + '..' +
            os.sep + 'testsubdir1' + os.sep,
        ]
        _cp = ConfigPath(replace=_sp)
        
        configdata = ConfigData(
            jval,
            datafile=_cp.get_config_filepath('testdata.json'),
            validator=MS_OFF,
            )

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


#
#######################
#
if __name__ == '__main__':
    unittest.main()
