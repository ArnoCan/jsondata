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


from jsondata import MS_OFF
from jsondata.jsonpointer import JSONPointer
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from filesysobjects.configdata import ConfigPath


class CallUnits(unittest.TestCase):

    def setUp(self):
        """Create an object for data only - no schema.
        rfc7159: Chapter 13, Example 1""
        """
        unittest.TestCase.setUp(self)
 
        _cp = ConfigPath(replace=os.path.dirname(__file__))
        self.datafile = _cp.get_config_filepath('rfc4627_8_02.json')
        self.configdata = ConfigData(
            [],
            datafile=self.datafile,
            validator=MS_OFF,
            )

    def testCase900(self):
        """Verify: rfc4627: Chapter 8, Example 2
        """
        jdoc = [
            {
                u'City': u'SAN FRANCISCO',
                u'Zip': u'94107',
                u'Country': u'US',
                u'precision': u'zip',
                u'Longitude': -122.3959,
                u'State': u'CA',
                u'Address': u'',
                u'Latitude': 37.7668
            },
            {
                u'City': u'SUNNYVALE',
                u'Zip': u'94085',
                u'Country': u'US',
                u'precision': u'zip',
                u'Longitude': -122.02602,
                u'State': u'CA',
                u'Address': u'',
                u'Latitude': 37.371991
            }
        ]

        assert self.configdata.data == jdoc

    def testCase902(self):
        """Access: rfc4627: Chapter 8, Example 2"""
        assert self.configdata.data[0] == {u'City': u'SAN FRANCISCO', u'Zip': u'94107', u'Country': u'US', u'precision': u'zip', u'Longitude': -122.3959, u'State': u'CA', u'Address': u'', u'Latitude': 37.7668}

    def testCase903(self):
        """Access: rfc4627: Chapter 8, Example 2"""
        assert self.configdata.data[0]['precision'] == "zip"

    def testCase904(self):
        """Access: rfc4627: Chapter 8, Example 2"""
        assert self.configdata.data[0]['Latitude'] == 37.7668
        assert self.configdata.data[0]['Longitude'] == -122.3959

    def testCase905(self):
        """Access: rfc4627: Chapter 8, Example 2"""
        assert self.configdata.data[0]['State'] == "CA"
        assert self.configdata.data[0]['Zip'] == "94107"
        assert self.configdata.data[0]['Country'] == "US"

    def testCase906(self):
        """Access: rfc4627: Chapter 8, Example 2"""
        assert self.configdata.data[0]['City'] == "SAN FRANCISCO"

    def testCase907(self):
        """Access: rfc4627: Chapter 8, Example 2"""
        assert self.configdata.data[0]['Address'] == ""

    def testCase908(self):
        """Access: rfc4627: Chapter 8, Example 2"""
        assert self.configdata.data[1] == {u'City': u'SUNNYVALE', u'Zip': u'94085', u'Country': u'US', u'precision': u'zip', u'Longitude': -122.02602, u'State': u'CA', u'Address': u'', u'Latitude': 37.371991}

    def testCase909(self):
        """Access: rfc4627: Chapter 8, Example 2"""
        assert self.configdata.data[1][u'precision'] == u"zip"
        assert self.configdata.data[1]['City'] == "SUNNYVALE"
        assert self.configdata.data[1]['State'] == "CA"
        assert self.configdata.data[1]['Zip'] == "94085"
        assert self.configdata.data[1]['Country'] == "US"

    def testCase910(self):
        """Access: rfc4627: Chapter 8, Example 2"""
        assert self.configdata.data[1]['Address'] == ""

    def testCase911(self):
        """Access: rfc4627: Chapter 8, Example 2"""
        assert self.configdata.data[1]['Latitude'] == 37.371991
        assert self.configdata.data[1]['Longitude'] == -122.026020

    def testCase912(self):
        """Access: rfc4627: Chapter 8, Example 2"""
        assert self.configdata.data[1]['precision'] == "zip"
        assert self.configdata.data[1]['Latitude'] == 37.371991
        assert self.configdata.data[1]['Longitude'] == -122.026020
        assert self.configdata.data[1]['Address'] == ""
        assert self.configdata.data[1]['City'] == "SUNNYVALE"
        assert self.configdata.data[1]['State'] == "CA"
        assert self.configdata.data[1]['Zip'] == "94085"
        assert self.configdata.data[1]['Country'] == "US"

    def testCase913(self):
        """Access: rfc4627: Chapter 8, Example 2"""
        assert self.configdata.data[0]['precision'] == "zip"
        assert self.configdata.data[0]['Latitude'] == 37.7668
        assert self.configdata.data[0]['Longitude'] == -122.3959
        assert self.configdata.data[0]['Address'] == ""
        assert self.configdata.data[0]['City'] == "SAN FRANCISCO"
        assert self.configdata.data[0]['State'] == "CA"
        assert self.configdata.data[0]['Zip'] == "94107"
        assert self.configdata.data[0]['Country'] == "US"

        assert self.configdata.data[1]['precision'] == "zip"
        assert self.configdata.data[1]['Latitude'] == 37.371991
        assert self.configdata.data[1]['Longitude'] == -122.026020
        assert self.configdata.data[1]['Address'] == ""
        assert self.configdata.data[1]['City'] == "SUNNYVALE"
        assert self.configdata.data[1]['State'] == "CA"
        assert self.configdata.data[1]['Zip'] == "94085"
        assert self.configdata.data[1]['Country'] == "US"


if __name__ == '__main__':
    unittest.main()
