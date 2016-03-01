"""Remove entries.
"""

from __future__ import absolute_import

import unittest
import os
import sys

import json,jsonschema
jval = None

from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData

# name of application, used for several filenames as default
_APPNAME = "jsondatacheck"
appname = _APPNAME
#
#######################
#
class CallUnits(unittest.TestCase):
    name=os.path.curdir+__file__

    output=True
    output=False

    def testCase000(self):
        """Check basics."""
        assert 0==0
        pass

    def testCase001(self):
        """Load main JSON data and JSONschema, and validate.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('datafile.json')
        schemafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('schema.jsd')

        kargs = {}
        kargs['configfile'] = datafile
        kargs['schemafile'] = schemafile
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = ConfigData.DEFAULT
        kargs['branchoperations'] = ConfigData.BRANCH_REMOVE
        configdata = ConfigData(appname,**kargs)

        assert repr(configdata.data) == "{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"
        pass

    def testCase002(self):
        """Load data file, use in-memory schema for validation.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        # branch to be loaded
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch0.json')

        # partial schema for branch
        schema = { 'phoneNumber':configdata.schema['properties']['phoneNumber'] }

        kargs = {}
        kargs['schema'] = schema
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = ConfigData.DEFAULT

        # May look weird for now, but import also can remove imported parts!
        kargs['branchoperations'] = ConfigData.BRANCH_REMOVE

        target = configdata.data
        configdata.import_data(datafile, None, target, **kargs)

        # Expected the nodes within the datafile to be removed.
        # No content is checked, just the complete tree is removed.
        conf_dat = "{u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"
        assert repr(configdata.data) == conf_dat


#
#######################
#
#
#######################
#
if __name__ == '__main__':
    unittest.main()
