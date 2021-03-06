# -*- coding: utf-8 -*-
"""Standards tests from RFC6902 for compliance of patch syntax.

"""
from __future__ import absolute_import

import unittest
import os

jval = None

try:
    from jsondata.JSONPointer import JSONPointer
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"
try:
    from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
    from jsondata.JSONDataSerializer import MODE_SCHEMA_OFF
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"

# name of application, used for several filenames as MODE_SCHEMA_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME
#
#######################
#
class CallUnits(unittest.TestCase):


    def testCase000(self):
        """Create an object for data only - no schema.
        """
        global configdata
        global appname

        kargs = {}
        kargs['datafile'] = os.path.dirname(__file__)+os.sep+'datafile.json'
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kargs)

        ref = """{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""

        assert ref == repr(configdata)


    def testCase001(self):
        """Create a new branch with value
        """
        global configdata
        global appname
        global jsonpatchlist

        #
        # create
        nbranch = configdata.branch_create(
                    JSONPointer("/phoneNumber").get_node(configdata.data),
                    JSONPointer("/-/skype/de"),
                    "hugo@skype") 
        
        nrepr = """u'hugo@skype'"""
        assert nrepr == repr(nbranch)
        
        crepr="""{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}, {u'skype': {u'de': u'hugo@skype'}}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert crepr == repr(configdata) 
        
        drepr="""{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}, {u'skype': {u'de': u'hugo@skype'}}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert drepr == repr(configdata.data) 

        assert crepr == drepr 


    def testCase002(self):
        """Test value
        """
        global configdata
        global appname
        global jsonpatchlist

        # variant A - referenz to the value
        A = JSONPointer("/phoneNumber/3/skype/de")
        A = A.get_node_or_value(configdata.data)
        ret = configdata.branch_test(A, "hugo@skype") 
        assert ret == True

        # variant B - reference to a logical JSON container node - array or object
        B = JSONPointer("/phoneNumber/3/skype/de")
        B = B.get_node(configdata.data,True)
        ret = configdata.branch_test(B['de'], "hugo@skype") 
        assert ret == True

#
#######################
#
if __name__ == '__main__':
    unittest.main()
