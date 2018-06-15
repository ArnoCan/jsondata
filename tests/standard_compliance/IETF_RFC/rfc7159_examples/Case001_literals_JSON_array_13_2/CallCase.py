# -*- coding: utf-8 -*-
"""Standards tests from RFC7159, Chapter 13, Example 2
"""
from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson
else:
    import json as myjson
import jsonschema


jval = None
configdata = None

try:
    from jsondata.jsonpointer import JSONPointer
except Exception as e:
    print("\n#\n#*** Set 'PYTHONPATH' (" + str(e) + ")\n#\n")
try:
    from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
except Exception as e:
    print("\n#\n#*** Set 'PYTHONPATH' (" + str(e) + ")\n#\n")
try:
    from jsondata.jsondata import MS_OFF
except Exception as e:
    print("\n#\n#*** Set 'PYTHONPATH' (" + str(e) + ")\n#\n")

# name of application, used for several filenames as MS_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME
#
#######################
#


class CallUnits(unittest.TestCase):

    def __init__(self, *args, **kargs):
        super(CallUnits, self).__init__(*args, **kargs)

    def setUp(self):
        global configdata
        global appname

        kargs = {}
        kargs['datafile'] = os.path.dirname(
            __file__) + os.sep + 'rfc7159_13_02.json'
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MS_OFF
        configdata = ConfigData(appname, **kargs)

    def testCase900(self):
        """Verify: rfc7159: Chapter 13, Example 2
        """
        version = '{0}.{1}'.format(*sys.version_info[:2])
        if version >= '2.7':  # pragma: no cover
            # due to a bug in python2.6.x
            jdoc = [{u'City': u'SAN FRANCISCO', u'Zip': u'94107', u'Country': u'US', u'precision': u'zip', u'Longitude': -122.3959, u'State': u'CA', u'Address': u'', u'Latitude': 37.7668}, {u'City': u'SUNNYVALE', u'Zip': u'94085', u'Country': u'US', u'precision': u'zip', u'Longitude': -122.02602, u'State': u'CA', u'Address': u'', u'Latitude': 37.371991}]
            assert configdata.data == jdoc

    def testCase902(self):
        """Access: rfc7159: Chapter 13, Example 2""
        """
        assert configdata.data[0] == {u'City': u'SAN FRANCISCO', u'Zip': u'94107', u'Country': u'US', u'precision': u'zip', u'Longitude': -122.3959, u'State': u'CA', u'Address': u'', u'Latitude': 37.7668}

    def testCase903(self):
        """Access: rfc7159: Chapter 13, Example 2""
        """
        assert configdata.data[0]['precision'] == "zip"

    def testCase904(self):
        """Access: rfc7159: Chapter 13, Example 2""
        """
        assert configdata.data[0]['Latitude'] == 37.7668
        assert configdata.data[0]['Longitude'] == -122.3959

    def testCase905(self):
        """Access: rfc7159: Chapter 13, Example 2""
        """
        assert configdata.data[0]['State'] == "CA"
        assert configdata.data[0]['Zip'] == "94107"
        assert configdata.data[0]['Country'] == "US"

    def testCase906(self):
        """Access: rfc7159: Chapter 13, Example 2""
        """
        assert configdata.data[0]['City'] == "SAN FRANCISCO"

    def testCase907(self):
        """Access: rfc7159: Chapter 13, Example 2""
        """
        assert configdata.data[0]['Address'] == ""

    def testCase908(self):
        """Access: rfc7159: Chapter 13, Example 2
        """
        assert configdata.data[1] == {u'City': u'SUNNYVALE', u'Zip': u'94085', u'Country': u'US', u'precision': u'zip', u'Longitude': -122.02602, u'State': u'CA', u'Address': u'', u'Latitude': 37.371991}

    def testCase909(self):
        """Access: rfc7159: Chapter 13, Example 2
        """
        assert configdata.data[1][u'precision'] == u"zip"
        assert configdata.data[1]['City'] == "SUNNYVALE"
        assert configdata.data[1]['State'] == "CA"
        assert configdata.data[1]['Zip'] == "94085"
        assert configdata.data[1]['Country'] == "US"

    def testCase910(self):
        """Access: rfc7159: Chapter 13, Example 2
        """
        assert configdata.data[1]['Address'] == ""

    def testCase911(self):
        """Access: rfc7159: Chapter 13, Example 2
        """
        assert configdata.data[1]['Latitude'] == 37.371991
        assert configdata.data[1]['Longitude'] == -122.026020

    def testCase912(self):
        """Access: rfc7159: Chapter 13, Example 2
        """
        assert configdata.data[1]['precision'] == "zip"
        assert configdata.data[1]['Latitude'] == 37.371991
        assert configdata.data[1]['Longitude'] == -122.026020
        assert configdata.data[1]['Address'] == ""
        assert configdata.data[1]['City'] == "SUNNYVALE"
        assert configdata.data[1]['State'] == "CA"
        assert configdata.data[1]['Zip'] == "94085"
        assert configdata.data[1]['Country'] == "US"

    def testCase913(self):
        """Access: rfc7159: Chapter 13, Example 2
        """
        assert configdata.data[0]['precision'] == "zip"
        assert configdata.data[0]['Latitude'] == 37.7668
        assert configdata.data[0]['Longitude'] == -122.3959
        assert configdata.data[0]['Address'] == ""
        assert configdata.data[0]['City'] == "SAN FRANCISCO"
        assert configdata.data[0]['State'] == "CA"
        assert configdata.data[0]['Zip'] == "94107"
        assert configdata.data[0]['Country'] == "US"

        assert configdata.data[1]['precision'] == "zip"
        assert configdata.data[1]['Latitude'] == 37.371991
        assert configdata.data[1]['Longitude'] == -122.026020
        assert configdata.data[1]['Address'] == ""
        assert configdata.data[1]['City'] == "SUNNYVALE"
        assert configdata.data[1]['State'] == "CA"
        assert configdata.data[1]['Zip'] == "94085"
        assert configdata.data[1]['Country'] == "US"


if __name__ == '__main__':
    unittest.main()
