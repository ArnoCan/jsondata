Abstract
########

The *jsondata* package provides standards based processing of JSON data
with emphasis on the management of modular structures including JSON-Pointer
and JSON-Patch.

The data is represented as in-memory tree structures with dynamically added
and removed components as branches. The data could be validated and stored 
for the later reuse.
The emphasis is on low resource consumption, thus
introcudes a slim layer covering the complex structure operations only, while the
data itself is native Python data compatible to *json*, *ujson* and *jsonschema*.

Supported main standards and drafts:

* JSON:  [RFC4627]_, [RFC7159]_, [RFC6901]_, [RFC6902]_,
  relative JSON Pointer [RELPOINTER]_ Draft v1 / 2018
* JSON schema: JSON schema [ZYP]_  Draft v4 / 2013

The supported platforms are:
 
* Linux, BSD, Unix, OS-X, Cygwin, and Windows
* Python2, Python3


Cockpit
#######

.. raw:: html

   <div class="indextab">

+--------------------------+--------------------------------------------------------------+---------------------+---------------------------+-----------------------------------------------+
| Component                | Standards/References                                         | HowTo               | shortcuts                 | API                                           |
+==========================+==============================================================+=====================+===========================+===============================================+
| `JSON Data`_             | [json]_ [ujson]_ [RFC8259]_ [RFC7159]_ [RFC4627]_ [ECMA404]_ | `Data`_             | :ref:`SCUT_JSONDATA`      | `jsondata.jsondata.JSONData`_                 |
+--------------------------+--------------------------------------------------------------+---------------------+---------------------------+-----------------------------------------------+
| `JSON Pointer`_          | [RFC6901]_                                                   | `Pointer`_          | :ref:`SCUT_JSONPOINTER`   | `jsondata.jsonpointer.JSONPointer`_           |
+--------------------------+--------------------------------------------------------------+---------------------+---------------------------+-----------------------------------------------+
| `JSON Relative Pointer`_ | [RELPOINTER]_ Draft v1 / 2018                                | `Relative Pointer`_ | :ref:`SCUT_JSONPOINTER`   | `jsondata.jsonpointer.JSONPointer`_           |
+--------------------------+--------------------------------------------------------------+---------------------+---------------------------+-----------------------------------------------+
| `JSON Patch`_            | [RFC6902]_                                                   | `Patch`_            | :ref:`SCUT_JSONPATCH`     | `jsondata.jsonpatch.JSONPatch`_               |
+--------------------------+--------------------------------------------------------------+---------------------+---------------------------+-----------------------------------------------+
| `JSON Schema`_           | [jsonschema]_ [ZYP]_  Draft v4 / 2013                        | `Schema`_           | :ref:`SCUT_JSONDATA`      | `jsondata.jsondata.JSONData`_                 |
+--------------------------+--------------------------------------------------------------+---------------------+---------------------------+-----------------------------------------------+
| `JSON Persistency`_      | Export and import documents and branches                     | `Serialize`_        | :ref:`SCUT_JSONSERIALIZE` | `jsondata.jsondataserializer.JSONSerializer`_ |
+--------------------------+--------------------------------------------------------------+---------------------+---------------------------+-----------------------------------------------+
| `JSON Package init`_     |                                                              |                     | :ref:`SCUT_JSONINI`       | `jsondata.__init__`_                          |
+--------------------------+--------------------------------------------------------------+---------------------+---------------------------+-----------------------------------------------+

+------------------------+------------------------+
| Artifacts              | Shortcuts              |
+========================+========================+
| Concepts and Design    | :ref:`DEVELOPMENTDOCS` |
+------------------------+------------------------+
| Programming Interfaces | :ref:`DEVELOPMENTAPI`  |
+------------------------+------------------------+

+----------------------------------+-----------------+
| Related Projects                 | External        |
+==================================+=================+
| Commandline Interface            | [jsoncli]_      |
+----------------------------------+-----------------+
| Compare and Analyse JSON Data    | [jsondatadiff]_ |
+----------------------------------+-----------------+
| Search JSON Pattern              | [jsondatafind]_ |
+----------------------------------+-----------------+
| Scan Commandline Options to JSON | [jsoncliopts]_  |
+----------------------------------+-----------------+
| Compute JSON Data                | [jsoncompute]_  |
+----------------------------------+-----------------+
| JSON Unit Tests                  | [jsondataunit]_ |
+----------------------------------+-----------------+

Introduced file suffixes.

+--------+----------------------+
| suffix |                      |
+========+======================+
| json   | JSON data file       |
+--------+----------------------+
| jsd    | JSON schema          |
+--------+----------------------+
| jsonp  | JSON patch - RFC6902 |
+--------+----------------------+

.. raw:: html

   </div>


.. _JSON Package init: jsondata_init_doc.html
.. _jsondata.__init__: jsondata_init_doc.html#

.. _Data: howto_class_jsondata.html
.. _Pointer: howto_class_jsonpointer.html 
.. _Relative Pointer: howto_class_jsonpointer_relative.html
.. _Patch: howto_class_jsonpatch.html
.. _Schema: howto_validate_json.html
.. _Serialize: howto_class_jsondataserializer.html 

.. _jsondata.jsondata.JSONData: jsondata_jsondata_doc.html 
.. _jsondata.jsonpointer.JSONPointer: jsondata_jsonpointer_doc.html
.. _jsondata.jsonpatch.JSONPatch: jsondata_jsonpatch_doc.html
.. _jsondata.jsondataserializer.JSONSerializer: jsondata_jsonserializer_doc.html

.. _JSON Data:jsondata_branch_operations.html
.. _JSON Pointer:jsondata_pointer_operations.html
.. _JSON Relative Pointer: jsondata_pointer_operations.html#relative-json-pointers
.. _JSON Schema: jsondata_integration.html
.. _JSON Persistency: jsondata_branch_serializer.html

.. _JSON data set algebra: jsondata_branch_operations.html#syntax-elements
.. _JSON Pointer algebra: jsondata_pointer_operations.html#syntax-elements
.. _JSON Patch set algebra: jsondata_patch_operations.html#syntax-elements

.. _Branch Algebra: howto_class_jsondata.html#branch-algebra
.. _Pointer Algebra:  howto_class_jsonpointer.html#pointer-algebra
.. _Patch Algebra:  howto_class_jsonpatch.html#patch-algebra



Blueprint
#########

The architecture is based on the interfaces of the packages *json* and
*jsonschema*, and compatible packages such as *ujson*. 

.. raw:: html

   <div class="blueprint">

.. parsed-literal::


                   +---------------------------------+
    Applications   |         application-layer       |    see e.g. [jsonlathe]_, [restdrill]_
    Middeware      +---------------------------------+  
    .   .  .  .  .  . | .  .  .  .  .| .  .  .  .  | .  .  .  .  .  .  .  .  .
                   + - - - - - - - - - - - - - - - - +    Libraries: [jsoncompute]_, [jsoncliopts]_, [jsondataunit]_, 
    Process JSON   |        processing tools         |    [jsondatadiff]_, [jsondatafind]_
                   + - - - - - - - - - - - - - - - - +    Command Line Interface: [jsoncli]_
    .   .  .  .  .  . | .  .  .  .  .| .  .  .  .  | .  .  .  .  .  .  .  .  .
                      |              V             |     
                      |  +----------------------+  |
    JSON Data         |  |       jsondata       |  |
      Data Structures |  |  `jsondata.jsondata <jsondata_branch_operations.html>`_   |  |      [RFC8259]_/[RFC7159]_/[RFC4627]_
      Pointer         |  | `jsondata.jsonpointer <jsondata_pointer_operations.html>`_ |  |      [RFC6901]_/draft-handrews-relative-json-pointer [RELPOINTER]_
      Patch           |  |  `jsondata.jsonpatch <jsondata_patch_operations.html>`_  |  |      [RFC6902]_
                      |  +----------------------+  |    
                      |         |       |          |      
    .  .  .  .  .  .  | .  .  . | .  .  | .  .  .  |  .  .  .  .  .  .  .  .  .
                      +----+----+       +-----+----+           
                           |                  |                           
                           V                  V                            
                   +----------------+-----------------+
    JSON           |     [json]_     |   [jsonschema]_  |    [RFC8259]_/[RFC7159]_/[RFC4627]_/[ECMA262]_/[ECMA404]_    
    Syntax         |     [ujson]_    |                 |    draft-zyp-json-schema-04 [ZYP]_   
                   +----------------+-----------------+ 

.. raw:: html

   </div>

The provided features comprise:

* `JSON Data <jsondata_branch_operations.html>`_ : Manage branches of substructures - jsondata.jsondata
  `[features] <jsondata_branch_operations.html#>`_
  `[API] <jsondata_jsondata_doc.html#>`_
  `[source] <_modules/jsondata/jsondata.html#JSONData>`_

* `JSON Serializer <jsondata_branch_serializer.html>`_ : Serialize JSON documents - jsondata.jsondataserializer 
  `[features] <jsondata_branch_serializer.html#>`_
  `[API] <jsondata_jsonserializer_doc.html#>`_
  `[source] <_modules/jsondata/jsondataSerializer.html#JSONDataSerializer>`_


* `JSON Pointer <jsondata_pointer_operations.html>`_ : Access pointer paths and values - jsondata.jsonpointer 
  `[features] <jsondata_pointer_operations.html#>`_
  `[API] <jsondata_jsonpointer_doc.html#>`_
  `[source] <_modules/jsondata/jsonpointer.html#JSONPointer>`_

* `JSON Patch <jsondata_patch_operations.html>`_ : Modify data structures and values - jsondata.jsonpatch 
  `[features] <jsondata_patch_operations.html#>`_
  `[API] <jsondata_jsonpatch_doc.html#>`_
  `[source] <_modules/jsondata/jsonpatch.html#JSONPatch>`_

The syntax primitives of underlying layers are processed by the imported standard packages *json* and *jsonschema* 
in conformance to related standards.
For the examples including from standards refer to `Howto <howto.html#>`_ .
For the architecture refer to `Software design <software_design.html>`_. 

Table of Contents
#################

.. toctree::
   :maxdepth: 2

   index_shortcuts
   index_jsondata
   index_testdata

   UseCases

   howto
   install

Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* `Glossary <glossary.html>`_
* `References <references.html>`_
* :ref:`search`


Resources
#########

.. include:: project.rst

**Online Documents**

* Pythonhosted: https://pythonhosted.org/timeatdate/

**Licenses**

* Artistic-License-2.0(base license): `ArtisticLicense20.html <_static/ArtisticLicense20.html>`_

* Forced-Fairplay-Constraints(amendments): `licenses-amendments.txt <_static/licenses-amendments.txt>`_ 

  |profileinfo|  [xkcd]_ Support the OpenSource Authors :-)

  .. |profileinfo| image:: _static/profile_info.png 
     :target: _static/profile_info.html
     :width: 48

**Downloads**

* Python Package Index: https://pypi.python.org/pypi/timeatdate
* Sourceforge.net: https://sourceforge.net/projects/timeatdate/

* github.com: https://github.com/ArnoCan/timeatdate/

