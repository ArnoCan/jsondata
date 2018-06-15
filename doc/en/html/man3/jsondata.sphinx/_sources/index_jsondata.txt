
'jsondata' - package
####################

.. toctree::
   :maxdepth: 4

The package 'jsondata' is aimed for the management of modular in-memory data 
structures based on JSON. The data is foreseen to be represented by a main data
tree with dynamically added and/or removed branches. The branches of data 
structures in particular provide for custom data. The data could either be 
related to a module, and/or to specific classes. The components provides by 
the package are:

* **JSONData**

  The main class JSONData provides for the core interface of the
  integration of JSON based documents and sub-documents including the 
  validation by JSONschema - RFC7159/RFC4629 and DRAFT4schema.
  This provides for dynamic incremental construction of data and 
  the persistent storage of the modified tree. The data is organized 
  into trees and branches managed by the packages 'json' and 'jsonschema'. 

* **JSONDataSerializer**

  The class JSONDataSerializer derived from JSONData provides for 
  serialization and integration of documents and sub-documents. This 
  provides for the persistent storage of modified document trees.

* **JSONPointer**

  The JSONPointer module provides for addressing of components within
  JSON based data structures in accordance to RCF7159 and RFC6901. 
  The integrated caching of the in-memory address of the pointed node
  provides for native speed in case of repetition, aimed for nested
  hierarchical loop constructs.
  The class JSONPointer in particular provides operators for pointer 
  arithmetics in order to simplify the application of navigation 
  and loop constructs.
  
* **JSONPatch**

  The JSONPatch module provides features for the alteration of JSON based
  data structures in accordance to RFC6902. The close design enables the
  fast addressing by combined usage with the class JSONPointer. 
  The class JSONPatch in particular provides operators for patch arithmetics
  in order to simplify the modular patch management and loop constructs.
  The patch task lists could be assembled by modules, modified as required 
  and stored persistently for reuse. 

The close design to the presented in-memory interface by the packages 'json'
and 'jsonschema' provides for reliable and fast access based on the standard 
Python packages, while the 'jsondata' package adds high-level abstractions
provided by standards for addressing and data assembly. The native Python 
access to the data entries remains compatible, while due to the 
caching of in-memory addresses of the nodes the access by the 'jsondata' 
add-ons is close to native Python performance. 

The package 'jsondata' supports the standards RFC6901, RFC6902, and the
integration of RFC7159 with DRAFT4Schema, while relying for the syntax
primitives of underlying layers presented by the packages 'json' and
'jsonschema'. The JSON language primitives for JSON are conform with
related ECMA and RFC standards and proposals. Here ECMA-262, ECMA-404, 
RFC7159/RFC4627, 'draft-zyp-json-schema-04', and others.

JSON based data provides for low resource data structure descriptions, 
thus fits in general quite good to distributed interface APIs, beneath 
JavaScript itself to protocols like those based on REST. But it also is 
applicable in case of numerous other requirements, a typical application
for branch data is the persistent storage of GUI models for 
dynamically loaded and released user elements.

The core module 'jsondata.jsondata' provides hereby the load of a master model from a JSON file, 
and the incremental addition and removal of branches to the model by loading additional 
JSON modules into the master model.
This is accompanied by the additional modules of this package, e.g. for modification in 
accordance to standards, or persistency of the in-memory data.
The implementation is based on the standard packages 'json' and 'jsonschema'.
The workflow provided by this package is:

#. Create the initial in-memory data model by loading the master JSON data.
   Decide here to use validation or not.
   Even though the validation itself could be shifted to a later state,
   once the data is loaded it may alter the state of the application
   irreversible.

#. Add/insert an arbitrary number of branches provided e.g. by plugins
   into an arbitrary position of the data model.
   Now for the branch decide whether to validate or not.

The data could be validated by provided JSONschema files. The interface
supports for various types of branch insertion and deletion.
The supported data resulting into a tree-structure could be depicted as::

    root-node
        |
    APP-schema
        +- <= import/export A-branches <-> API-schema + A-schema
        |
        +- <= import/export B-branches <-> API-schema + B-schema
        |
        `- <= import/export C-branches <-> API-schema + C-schema


In case of requested validation of multiple components various schema 
files are required.
The main schema for the application 'APP-schema' has to be provided
for the core application.

The APP-schema provides in case of persistent configuration data the
structural model for the statically related data of the application
code. The 'datafile' with values, e.g. altered by user
interaction, could be varied and superposed as required, as long
as the structure is valid.
The import interface represented in 'API-schema' is for the case of
validation mandatory too. This ensures valid interface data is
imported into the application. Whereas the specific schema
files(A,B,C-schema) depend on the actual implementation of the imported modules.
The resulting data could be saved for later reuse.


.. toctree::
   :maxdepth: 2

   jsondata_init_doc.rst
   jsondata_jsondata_doc.rst
   jsondata_jsonserializer_doc.rst
   jsondata_jsonpointer_doc.rst
   jsondata_jsonpatch_doc.rst

