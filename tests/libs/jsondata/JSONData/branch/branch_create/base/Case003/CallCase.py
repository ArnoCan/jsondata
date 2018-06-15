# -*- coding: utf-8 -*-
"""Standards tests from RFC6902 for compliance of patch syntax.

"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import unittest
import os

from filesysobjects.configdata import ConfigPath
from jsondata.jsondataserializer import JSONDataSerializer as ConfigData
from jsondata  import MS_OFF
from jsondata.jsonpointer import JSONPointer


class CallUnits(unittest.TestCase):

    def testCase000(self):

        _cp = ConfigPath(replace=os.path.dirname(__file__))
        datafile = _cp.get_config_filepath('datafile.json')
        configdata = ConfigData(
            {},
            datafile=datafile,
            validator=MS_OFF,
            )

        ref = {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
               'phoneNumber': [{'type': 'home', 'number': '212 555-1234'},
                               {'type': 'office', 'number': '313 444-555'},
                               {'type': 'mobile', 'number': '777 666-555'}]}

        assert ref == configdata

        nbranch = configdata.branch_create(
            JSONPointer("/-/skype/-"),
            JSONPointer("/phoneNumber")(configdata.data),
            "hugo@skype")

        ref =  {'address': {'streetAddress': '21 2nd Street', 'city': 'New York', 'houseNumber': 12}, 
                'phoneNumber': [{'type': 'home', 'number': '212 555-1234'},
                                {'type': 'office', 'number': '313 444-555'},
                                {'type': 'mobile', 'number': '777 666-555'},
                                {'skype': ['hugo@skype']}]}

        assert ref == configdata


#
#######################
#
if __name__ == '__main__':
    unittest.main()
