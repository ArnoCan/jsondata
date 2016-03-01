"""import of branches by jsondata.JSONDataSerializer.add()
"""
from __future__ import absolute_import

import unittest
import os
#import sys

#import json,jsonschema
jval = None

from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData

# name of application, used for several filenames as default
_APPNAME = "jsondatacheck"
appname = _APPNAME
#
#######################
#
class CallUnits(unittest.TestCase):
    """Base branch import by add.
    """
    name=os.path.curdir+__file__

    output=True
    output=False

    def testCase000(self):
        """Base environment verification"""
        assert 0==0
        pass

    def testCase001(self):
        """Load initial main/master data, and validate it with standard validator.
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
        kargs['branchoperations'] = ConfigData.BRANCH_ADD

        configdata = ConfigData(appname,**kargs)

        assert repr(configdata.data) == "{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"
        pass

    def testCase002(self):
        """Import a branch into initial main/master data, and validate it with standard validator.

        Do not insert '$schema' key.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        # branch to be loaded
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch0.json')

        # partial schema for branch, use here a subtree of main schema,
        # the entry:
        #    "$schema": "http://json-schema.org/draft-03/schema",
        # seems not to be required, else it has to be included
        schema = { 'phoneNumber':configdata.schema['properties']['phoneNumber'] }

        # import settings
        kargs = {}
        kargs['schema'] = schema
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = ConfigData.DEFAULT
        kargs['branchoperations'] = ConfigData.BRANCH_ADD

        # target container
        target = configdata.data

        # do it...
        # REMARK: schemafile is here None, because we use an in memory schema,
        #         and do not export - for now
        #
        # Expect False, because the node is already present, thus 'add'
        # has to fail.
        ret = configdata.import_data(datafile, None, target, **kargs)
        assert ret == False

        # expected - after add
        conf_dat = "{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"
        assert repr(configdata.data) == conf_dat

    def testCase003(self):
        """Import a branch into initial main/master data, and validate it with standard validator.

        Apply '$schema' key for branch/subtree of master schema.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        # branch to be loaded
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch0.json')

        # partial schema for branch, use here a subtree of main schema,
        # the entry:
        #    "$schema": "http://json-schema.org/draft-03/schema",
        # seems not to be required,
        #
        # but here just check it
        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            'phoneNumber':configdata.schema['properties']['phoneNumber']
        }

        # import settings
        kargs = {}
        kargs['schema'] = schema
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = ConfigData.DEFAULT
        kargs['branchoperations'] = ConfigData.BRANCH_ADD

        # target container
        target = configdata.data

        # do it...
        # REMARK: schemafile is here None, because we use an in memory schema,
        #         and do not export - for now
        configdata.import_data(datafile, None, target, **kargs)

        # expected - after add
        conf_dat = "{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"
        assert repr(configdata.data) == conf_dat

#
#######################
#
#
#######################
#
if __name__ == '__main__':
    unittest.main()
