.. _HOWTO_JSONMODULAR:

Modular JSON
============
One of the unique features of the package *jsondata* is it's consequent
adjustment to the management and processing of data structures called *branches*.
This enables modular JSON data and easy includes, imports, and exports of sub-trees.

.. toctree::
   :maxdepth: 2

   howto_modular_json

JSON Modules and Branches
-------------------------
The *jsondata* handles each structure as a *branch* - including the whole document,
which is seen as the master branch.
Therefore each JSON document - either seiralized, or in-memory - could be imported
to any JSON data structure.

Import JSON Modules as Branches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The import of a module into an existing JSON structure simply requires one call only.

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

   #
   # *** Modules as branches ***
   #
   
   # branches to be added
   branch1_datafile = os.path.abspath(os.path.dirname(
       __file__)) + os.sep + str('branch1.json')
   
   branch2_datafile = os.path.abspath(os.path.dirname(
       __file__)) + os.sep + str('branch2.json')
   
   
   # load branch data into memory
   jsondata.json_import(branch1_datafile)
   
   # load branch data into memory
   jsondata.json_import(branch2_datafile)
   
   print(jsondata)


Export JSON Branches as Modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The export of branch works similar as the import.
Just add the following lines to the previous example.

.. code-block:: python
   :linenos:

   outfile = os.path.abspath(os.path.dirname(
       __file__)) + os.sep + str('out_address.json')
   
   jsondata.json_export(outfile, "/address", pretty=False, force=True)


Copy and Modify JSON Modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The JSON modules are treated as *branches* once they are loaded into the memory.
For the in-memory operationd the methods and operators are provided by the base
class of the serializer the class *JSONData*.

See :ref:`HOWTO_JSONDATA`.

Validate Modules by one Main JSON Schema
----------------------------------------
The simples way of using schemas is to provide one schema for the whole data 
structure - which could raise the complexity by this one schema itself.
The single schema requires the description of the whole document including
any expected variant.

The following example demonstrates the repetitive validation of a JSON structure
by a single schema loaded once during the initialization of the object 
created by *JSONData*.
This is either set by the initialization as default for all import calls,
of provided as a parameter for each import call individually.
Add these lines to one of the previous examples.

.. code-block:: python
   :linenos:

   from jsondata import MS_DRAFT4

   #
   # *** Modules as branches ***
   #
   
   # branches to be added
   branch1_datafile = os.path.abspath(os.path.dirname(
       __file__)) + os.sep + str('branch1.json')
   
   branch2_datafile = os.path.abspath(os.path.dirname(
       __file__)) + os.sep + str('branch2.json')
   
   
   # load branch data into memory
   jsondata.json_import(branch1_datafile, validator="draft4")
   
   # load branch data into memory
   jsondata.json_import(branch2_datafile, validator=MS_DRAFT4)
   
   print(jsondata)


Validate Modules by Modular JSON Schema
---------------------------------------
The *jsondata* provides in addition for the validation call by call,
where each call could uuse a different schema related to the current
branch only.

Modular JSON Schemes
^^^^^^^^^^^^^^^^^^^^

Import a Schema Module
^^^^^^^^^^^^^^^^^^^^^^

Export a Schema Module
^^^^^^^^^^^^^^^^^^^^^^

Automate Module Processing with JSON Patch
------------------------------------------

