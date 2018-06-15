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
        self.datafile = _cp.get_config_filepath('testdata.json')
        self.schemafile = _cp.get_config_filepath('testdata.jsd')
        self.configdata = ConfigData(
            {},
            datafile=self.datafile,
            schemafile=self.schemafile,
            validator=MS_OFF,
            )

        # load data
        with open(self.datafile) as data_file:
            self.jval = myjson.load(data_file)
        if self.jval == None:
            raise BaseException("Failed to load data:" + str(data_file))

        assert self.jval

    def testCase920(self):
        """Access some entries by dynamic references from raw data file read.
        """
        global configdata

        # print "#---------------a"
        for l in ['domestic', 'abroad', ]:
            for n in [0, 1, ]:
                cdata = self.configdata.data["customers"][l][n]["name"]
                jdata = self.jval["customers"][l][n]["name"]
                assert cdata == jdata

                # now pointer
                px = JSONPointer(u'/customers/' + unicode(l) +
                                 u'/' + unicode(n) + JSONPointer('/name'))
                vx = px.get_node_value(self.configdata.data)
                assert self.configdata.data["customers"][l][n]["name"] == vx

                vx = JSONPointer(u'/customers/' + unicode(l) + u'/' + unicode(n) +
                                 JSONPointer('/name')).get_node_value(self.configdata.data)
                assert self.configdata.data["customers"][l][n]["name"] == vx

                assert self.configdata.data["customers"][l][n]["name"] == JSONPointer(
                    u'/customers/' + unicode(l) + u'/' + unicode(n) + JSONPointer('/name')).get_node_value(self.configdata.data)

                # now pointer with add
                jp = '/customers/' + \
                    unicode(l) + u'/' + unicode(n) + JSONPointer('/name')
                assert self.configdata.data["customers"][l][n]["name"] == JSONPointer(
                    jp).get_node_value(self.configdata.data)

                # now pointer with add
                assert self.configdata.data["customers"][l][n]["name"] == JSONPointer(
                    '/customers/' + unicode(l) + u'/' + unicode(n) + JSONPointer('/name')).get_node_value(self.configdata.data)

                cdata = self.configdata.data["customers"][l][n]["industries"]
                jdata = self.configdata.data["customers"][l][n]["industries"]
                assert cdata == jdata

                # now pointer
                assert self.configdata.data["customers"][l][n]["industries"] == JSONPointer(
                    '/customers/' + str(l) + u'/' + str(n) + JSONPointer('/industries')).get_node_value(self.configdata.data)

                # now pointer add
                assert self.configdata.data["customers"][l][n]["industries"] == (JSONPointer(
                    '/customers') + l + n + 'industries').get_node_value(self.configdata.data)

                for p in [0, 1, ]:
                    cdata = self.configdata.data["customers"][l][n]["products"][p]["name"]
                    jdata = self.configdata.data["customers"][l][n]["products"][p]["name"]
                    assert cdata == jdata

                    # now pointer
                    assert self.configdata.data["customers"][l][n]["products"][p]["name"] == JSONPointer(
                        '/customers/' + str(l) + '/' + str(n) + '/products/' + str(p) + '/name').get_node_value(self.configdata.data)

                    cdata = self.configdata.data["customers"][l][n]["products"][p]["quantities"]
                    jdata = self.configdata.data["customers"][l][n]["products"][p]["quantities"]
                    assert cdata == jdata

                    # now pointer
                    assert self.configdata.data["customers"][l][n]["products"][p]["quantities"] == JSONPointer(
                        '/customers/' + str(l) + '/' + str(n) + '/products/' + str(p) + '/quantities').get_node_value(self.configdata.data)

                    cdata = self.configdata.data["customers"][l][n]["products"][p]["priority"]
                    jdata = self.configdata.data["customers"][l][n]["products"][p]["priority"]
                    assert cdata == jdata

                    # now pointer
                    assert self.configdata.data["customers"][l][n]["products"][p]["priority"] == JSONPointer(
                        '/customers/' + str(l) + '/' + str(n) + '/products/' + str(p) + '/priority').get_node_value(self.configdata.data)


#
#######################
#
if __name__ == '__main__':
    unittest.main()
