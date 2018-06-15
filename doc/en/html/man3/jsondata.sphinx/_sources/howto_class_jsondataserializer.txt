JSONDataSerializer - JSON Persistency
=====================================

The class *JSONDataSerializer* provides persistency and modularity
for JSON data structures and branches.


.. toctree::
   :maxdepth: 2

      howto_class_jsondataserializer

Load
----
JSON data can be simply loaded from a file, which is either formatted as structured
tree view, or a simple (long-) line containing the whole JSON data.

The JSON data:

.. code-block:: json
   :linenos:

   {
     "address":{
       "streetAddress": "21 2nd Street",
       "city":"New York",
       "houseNumber":12
     },
     "phoneNumber":
       [
       {
         "type":"home",
         "number":"212 555-1234"
       },
       {
         "type":"office",
         "number":"313 444-555"
       },
       {
         "type":"mobile",
         "number":"777 666-555"
       }
     ]
   }
   
is easily loaded by the code:

.. code-block:: python
   :linenos:

   # -*- coding:utf-8   -*-
   from __future__ import absolute_import
   from __future__ import print_function
   
   import os
   
   from jsondata.jsondataserializer import JSONDataSerializer
   from jsondata  import MS_DRAFT4
   
   # name of application, used for several filenames as MS_DRAFT4
   appname = "jsondc"
   
   
   # JSON data
   datafile = os.path.abspath(os.path.dirname(
       __file__)) + os.sep + str('datafile.json')
   
   # JSON schema
   schemafile = os.path.abspath(os.path.dirname(
       __file__)) + os.sep + str('schema.jsd')
   
   # standard call options
   kargs = {}
   kargs['datafile'] = datafile
   kargs['schemafile'] = schemafile
   kargs['nodefaultpath'] = True
   kargs['nosubdata'] = True
   kargs['pathlist'] = os.path.dirname(__file__)
   kargs['validator'] = MS_DRAFT4
   
   # load JSON file
   jsondata = JSONDataSerializer(appname, **kargs)
   
   print(jsondata)

   pass



Save
----
The data e.g. as loaded by the previous example could be easily stored in a file
by the following code.
Just append the lines to the previous example.

.. code-block:: python
   :linenos:

   outfile = os.path.abspath(os.path.dirname(
       __file__)) + os.sep + str('outfile.json')
   
   jsondata.json_export(outfile, pretty=False, force=True)


Import and Export Branches
--------------------------
The package *jsondata* makes it inparticular easy to import and export subtrees 
called *branches* into/from a JSON data structucture.

For examples see :ref:`HOWTO_JSONMODULAR`.

Validation of Branches By JSON Schemes
--------------------------------------

The package *jsondata* provides either for the validation of the whole JSON data by
one schema, or the modular validation of sub-branches by multiple schemes.

For examples see :ref:`HOWTO_JSONMODULAR`.
