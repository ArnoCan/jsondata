.. raw:: html

   <div class="shortcuttab">

.. _DEVELOPMENTDOCS:

Development Documents
=====================
The *jsondata* paclkage provides for the structure operations on JSON data.

Concepts and Design
-------------------
* `Software design <software_design.html>`_ 

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

* `Integration with Standard Libraries <jsondata_integration.html>`_

API
---
* `jsondata <jsondata_init_doc.html>`_
* `jsondata.jsondata <jsondata_jsondata_doc.html>`_
* `jsondata.jsondataserializer <jsondata_jsonserializer_doc.html>`_
* `jsondata.jsonpatch <jsondata_jsonpatch_doc.html>`_
* `jsondata.jsonpointer <jsondata_jsonpointer_doc.html>`_
* `API in javadoc-style <epydoc/index.html>`_

Examples
--------
* `HowTo - Typical call examples <howto.html>`_

* Selected Common UsesCases `[examples] <usecases.html>`_

* Test data `[testdata] <#test-data>`_


.. _DEVELOPMENTAPI:

.. _SCUT_JSONINI:

jsondata
========

+--------------------+--------------------------+
| [docs]             | [source]                 |
+====================+==========================+
| `jsondata module`_ | `jsondata.__init__ (0)`_ |
+--------------------+--------------------------+

.. _jsondata module: jsondata_init_doc.html#
.. _jsondata.__init__ (0): _modules/jsondata/__init__.html#

.. _SCUT_JSONDATA:

jsondata.jsondata
=================

JSONData
--------
Provides operations modes in accordance to *RFC7159* [RFC7159]_ and *RFC4627* [RFC4627]_.

Attributes
^^^^^^^^^^
The slim wrapper only around the attributes of native data structures:

* *JSONData.data* - a reference to the in-memory JSON data,
  compatible to *json* [json]_ and *ujson* [ujson]_.
* *JSONData.schema* - a reference to an optional schema based on
  *jsonschema* [jsonschema]_.


Methods
^^^^^^^
  
Basic
"""""

+----------------+-------------------------+-----------------+
| [docs]         | [source]                | [op-unit-scope] |
+================+=========================+=================+
| `JSONData()`_  | `JSONData.__init__`_    |                 |
+----------------+-------------------------+-----------------+
| `__repr__`_    | `JSONData.__repr__`_    | B,A             |
+----------------+-------------------------+-----------------+
| `__str__`_     | `JSONData.__str__`_     | B,A             |
+----------------+-------------------------+-----------------+
| `get_data`_    | `JSONData.get_data`_    |                 |
+----------------+-------------------------+-----------------+
| `get_schema`_  | `JSONData.get_schema`_  |                 |
+----------------+-------------------------+-----------------+
| `dump_data`_   | `JSONData.dump_data`_   | A               |
+----------------+-------------------------+-----------------+
| `dump_schema`_ | `JSONData.dump_schema`_ |                 |
+----------------+-------------------------+-----------------+
| `set_schema`_  | `JSONData.set_schema`_  |                 |
+----------------+-------------------------+-----------------+
| `validate`_    | `JSONData.validate`_    | B,A             |
+----------------+-------------------------+-----------------+

The column *[op-unit-scope]* depicts the types and levels of provided operations:

* A: attribute 
* B: branch

Branches and Trees
""""""""""""""""""

+------------------------+---------------------------------+-----------------+----------------------+
| [docs]                 | [source]                        | [op-unit-scope] | [equivalet-operator] |
+========================+=================================+=================+======================+
| `branch_add`_          | `JSONData.branch_add`_          | B               | add                  |
+------------------------+---------------------------------+-----------------+----------------------+
| `branch_copy`_         | `JSONData.branch_copy`_         | B               | cp                   |
+------------------------+---------------------------------+-----------------+----------------------+
| `branch_create`_       | `JSONData.branch_create`_       | B               | new                  |
+------------------------+---------------------------------+-----------------+----------------------+
| `branch_move`_         | `JSONData.branch_move`_         | B               | mv                   |
+------------------------+---------------------------------+-----------------+----------------------+
| `branch_remove`_       | `JSONData.branch_remove`_       | B               | del                  |
+------------------------+---------------------------------+-----------------+----------------------+
| `branch_replace`_      | `JSONData.branch_replace`_      | B               | replace              |
+------------------------+---------------------------------+-----------------+----------------------+
| `branch_superpose`_    | `JSONData.branch_superpose`_    | B               | all-ops              |
+------------------------+---------------------------------+-----------------+----------------------+
| `branch_test`_         | `JSONData.branch_test`_         | B               | test                 |
+------------------------+---------------------------------+-----------------+----------------------+
| `copy`_                | `JSONData.copy`_                | B               | cp                   |
+------------------------+---------------------------------+-----------------+----------------------+
| `deepcopy`_            | `JSONData.deepcopy`_            | B               | cp                   |
+------------------------+---------------------------------+-----------------+----------------------+
| `get_canonical_value`_ | `JSONData.get_canonical_value`_ | B               |                      |
+------------------------+---------------------------------+-----------------+----------------------+
| `pop`_                 | `JSONData.pop`_                 |                 | pop                  |
+------------------------+---------------------------------+-----------------+----------------------+

Operators
^^^^^^^^^
Evaluation Operators
""""""""""""""""""""
+------------------+-------------+----------------------+-----------------+
| [logic-operator] | [docs]      | [source]             | [op-unit-scope] |
+==================+=============+======================+=================+
| exec             | `__call__`_ | `JSONData.__call__`_ | A               |
+------------------+-------------+----------------------+-----------------+

Comparison Operators
""""""""""""""""""""
+------------------+-----------+--------------------+-----------------+
| [logic-operator] | [docs]    | [source]           | [op-unit-scope] |
+==================+===========+====================+=================+
| ==               | `__eq__`_ | `JSONData.__eq__`_ | B,A             |
+------------------+-----------+--------------------+-----------------+
| !=               | `__ne__`_ | `JSONData.__ne__`_ | B,A             |
+------------------+-----------+--------------------+-----------------+

Items
^^^^^

+----------------+-------------------+----------------------------+-----------------+
| [operator]     | [docs]            | [source]                   | [op-unit-scope] |
+================+===================+============================+=================+
| del S[x]       | `__delitem__`_    | `JSONData.__delitem__`_    | B,A             |
+----------------+-------------------+----------------------------+-----------------+
| __iter__       | `__iter__`_       | `JSONData.__iter__`_       | B,A             |
+----------------+-------------------+----------------------------+-----------------+
| S[x]           | `__getitem__`_    | `JSONData.__getitem__`_    | B,A             |
+----------------+-------------------+----------------------------+-----------------+
| S[x] = v       | `__setitem__`_    | `JSONData.__setitem__`_    | B,A             |
+----------------+-------------------+----------------------------+-----------------+
| get_data_items | `get_data_items`_ | `JSONData.get_data_items`_ | B,A             |
+----------------+-------------------+----------------------------+-----------------+

.. _JSONData(): jsondata_jsondata_doc.html#jsondata.jsondata.JSONData.__init__
.. _JSONData.__call__: _modules/jsondata/jsondata.html#JSONData.__call__
.. _JSONData.__delitem__: _modules/jsondata/jsondata.html#JSONData.__delitem__
.. _JSONData.__eq__: _modules/jsondata/jsondata.html#JSONData.__eq__
.. _JSONData.__getitem__: _modules/jsondata/jsondata.html#JSONData.__getitem__
.. _JSONData.__init__: _modules/jsondata/jsondata.html#JSONData.__init__
.. _JSONData.__iter__: _modules/jsondata/jsondata.html#JSONData.__iter__
.. _JSONData.__ne__: _modules/jsondata/jsondata.html#JSONData.__ne__
.. _JSONData.__repr__: _modules/jsondata/jsondata.html#JSONData.__repr__
.. _JSONData.__setitem__: _modules/jsondata/jsondata.html#JSONData.__setitem__
.. _JSONData.__str__: _modules/jsondata/jsondata.html#JSONData.__str__
.. _JSONData.branch_add: _modules/jsondata/jsondata.html#JSONData.branch_add
.. _JSONData.branch_copy: _modules/jsondata/jsondata.html#JSONData.branch_copy
.. _JSONData.branch_create: _modules/jsondata/jsondata.html#JSONData.branch_create
.. _JSONData.branch_move: _modules/jsondata/jsondata.html#JSONData.branch_move
.. _JSONData.branch_remove: _modules/jsondata/jsondata.html#JSONData.branch_remove
.. _JSONData.branch_replace: _modules/jsondata/jsondata.html#JSONData.branch_replace
.. _JSONData.branch_superpose: _modules/jsondata/jsondata.html#JSONData.branch_superpose
.. _JSONData.branch_test: _modules/jsondata/jsondata.html#JSONData.branch_test
.. _JSONData.copy: _modules/jsondata/jsondata.html#JSONData.copy
.. _JSONData.deepcopy: _modules/jsondata/jsondata.html#JSONData.deepcopy
.. _JSONData.get_canonical_value: _modules/jsondata/jsondata.html#JSONData.get_canonical_value
.. _JSONData.get_data: _modules/jsondata/jsondata.html#JSONData.get_data
.. _JSONData.get_data_items: _modules/jsondata/jsondata.html#JSONData.get_data_items
.. _JSONData.get_schema: _modules/jsondata/jsondata.html#JSONData.get_schema
.. _JSONData.pop: _modules/jsondata/jsondata.html#JSONData.pop
.. _JSONData.dump_data: _modules/jsondata/jsondata.html#JSONData.dump_data
.. _JSONData.dump_schema: _modules/jsondata/jsondata.html#JSONData.dump_schema
.. _JSONData.set_schema: _modules/jsondata/jsondata.html#JSONData.set_schema
.. _JSONData.validate: _modules/jsondata/jsondata.html#JSONData.validate
.. _\__call__: jsondata_jsondata_doc.html#jsondata.jsondata.JSONData.__call__
.. _\__delitem__: jsondata_jsondata_doc.html#jsondata.jsondata.JSONData.__delitem__
.. _\__eq__: jsondata_jsondata_doc.html#jsondata.jsondata.JSONData.__eq__
.. _\__getitem__: jsondata_jsondata_doc.html#jsondata.jsondata.JSONData.__getitem__
.. _\__iter__: jsondata_jsondata_doc.html#jsondata.jsondata.JSONData.__iter__
.. _\__ne__: jsondata_jsondata_doc.html#jsondata.jsondata.JSONData.__ne__
.. _\__repr__: jsondata_jsondata_doc.html#jsondata.jsondata.JSONData.__repr__
.. _\__setitem__: jsondata_jsondata_doc.html#jsondata.jsondata.JSONData.__setitem__
.. _\__str__: jsondata_jsondata_doc.html#jsondata.jsondata.JSONData.__str__
.. _branch_add: jsondata_jsondata_doc.html#branch-add
.. _branch_copy: jsondata_jsondata_doc.html#branch-copy
.. _branch_create: jsondata_jsondata_doc.html#branch-create
.. _branch_move: jsondata_jsondata_doc.html#branch-move
.. _branch_remove: jsondata_jsondata_doc.html#branch-remove
.. _branch_replace: jsondata_jsondata_doc.html#branch-replace
.. _branch_superpose: jsondata_jsondata_doc.html#branch-superpose
.. _branch_test: jsondata_jsondata_doc.html#branch-test
.. _copy: jsondata_jsondata_doc.html#copy
.. _deepcopy: jsondata_jsondata_doc.html#deepcopy
.. _get_canonical_value: jsondata_jsondata_doc.html#get-canonical-value
.. _get_data: jsondata_jsondata_doc.html#get-data
.. _get_data_items: jsondata_jsondata_doc.html#jsondata.jsondata.JSONData.get_data_items
.. _get_schema: jsondata_jsondata_doc.html#jsondata.jsondata.JSONData.get_schema
.. _pop: jsondata_jsondata_doc.html#pop
.. _print_data: jsondata_jsondata_doc.html#print-data
.. _print_schema: jsondata_jsondata_doc.html#jsondata.jsondata.JSONData.dump_schema
.. _set_schema: jsondata_jsondata_doc.html#jsondata.jsondata.JSONData.set_schema
.. _validate: jsondata_jsondata_doc.html#validate


.. _SCUT_JSONSERIALIZE:

jsondata.jsondataserializer
===========================

JSONDataSerializer
------------------
Is derived from *JSONData*, provides persistency and schema validation.

Methods
^^^^^^^
Basic
"""""

+-----------------------+-----------------------------------+
| [docs]                | [source]                          |
+=======================+===================================+
| `JSONDataSerializer`_ | `JSONDataSerializer.__init__`_    |
+-----------------------+-----------------------------------+
| `dump_data`_          | `JSONDataSerializer.dump_data`_   |
+-----------------------+-----------------------------------+
| `dump_schema`_        | `JSONDataSerializer.dump_schema`_ |
+-----------------------+-----------------------------------+
| `set_schema (1)`_     | `JSONDataSerializer.set_schema`_  |
+-----------------------+-----------------------------------+

Import/Export
"""""""""""""

+----------------+-----------------------------------+
| [docs]         | [source]                          |
+================+===================================+
| `json_export`_ | `JSONDataSerializer.json_export`_ |
+----------------+-----------------------------------+
| `json_import`_ | `JSONDataSerializer.json_import`_ |
+----------------+-----------------------------------+

.. _JSONDataSerializer.__init__: _modules/jsondata/jsondataserializer.html#JSONDataSerializer.__init__
.. _JSONDataSerializer.json_export: _modules/jsondata/jsondataserializer.html#JSONDataSerializer.json_export
.. _JSONDataSerializer.json_import: _modules/jsondata/jsondataserializer.html#JSONDataSerializer.json_import
.. _JSONDataSerializer.dump_data: _modules/jsondata/jsondataserializer.html#JSONDataSerializer.dump_data
.. _JSONDataSerializer.dump_schema: _modules/jsondata/jsondataserializer.html#JSONDataSerializer.dump_schema
.. _JSONDataSerializer.set_schema: _modules/jsondata/jsondataserializer.html#JSONDataSerializer.set_schema
.. _JSONDataSerializer: jsondata_jsonserializer_doc.html#jsondata.jsondataserializer.JSONDataSerializer.__init__
.. _json_export: jsondata_jsonserializer_doc.html#jsondata.jsondataserializer.JSONDataSerializer.json_export
.. _json_import: jsondata_jsonserializer_doc.html#jsondata.jsondataserializer.JSONDataSerializer.json_import
.. _dump_data: jsondata_jsonserializer_doc.html#jsondata.jsondataserializer.JSONDataSerializer.dump_data
.. _dump_schema: jsondata_jsonserializer_doc.html#jsondata.jsondataserializer.JSONDataSerializer.dump_schema
.. _set_schema (1): jsondata_jsonserializer_doc.html#jsondata.jsondataserializer.JSONDataSerializer.set_schema


.. _SCUT_JSONPATCH:

jsondata.jsonpatch
==================
Supports *RFC6902* [RFC6902]_.

JSONPatchItem
-------------

Methods
^^^^^^^

Basic
"""""
+------------------+---------------------------+------------------+
| [docs]           | [source]                  | [logic-operator] |
+==================+===========================+==================+
| `JSONPatchItem`_ | `JSONPatchItem.__init__`_ |                  |
+------------------+---------------------------+------------------+
| `__repr__ (2)`_  | `JSONPatchItem.__repr__`_ | repr             |
+------------------+---------------------------+------------------+
| `__str__ (2)`_   | `JSONPatchItem.__str__`_  | str              |
+------------------+---------------------------+------------------+

Basic
"""""
+--------------------+------------------------------+------------------+
| [docs]             | [source]                     | [logic-operator] |
+====================+==============================+==================+
| `apply (2)`_       | `JSONPatchItem.apply`_       |                  |
+--------------------+------------------------------+------------------+
| `repr_export (2)`_ | `JSONPatchItem.repr_export`_ |                  |
+--------------------+------------------------------+------------------+
| `str_export (2)`_  | `JSONPatchItem.str_export`_  |                  |
+--------------------+------------------------------+------------------+

Operators
^^^^^^^^^
+--------------------+------------------------------+------------------+
| [docs]             | [source]                     | [logic-operator] |
+====================+==============================+==================+
| `__call__ (2)`_    | `JSONPatchItem.__call__`_    | exec             |
+--------------------+------------------------------+------------------+
| `__eq__ (2)`_      | `JSONPatchItem.__eq__`_      | ==               |
+--------------------+------------------------------+------------------+
| `__getitem__ (2)`_ | `JSONPatchItem.__getitem__`_ | [i]              |
+--------------------+------------------------------+------------------+
| `__ne__ (2)`_      | `JSONPatchItem.__ne__`_      | !=               |
+--------------------+------------------------------+------------------+

.. _JSONPatchItem.__call__: _modules/jsondata/jsonpatch.html#JSONPatchItem.__call__
.. _JSONPatchItem.__eq__: _modules/jsondata/jsonpatch.html#JSONPatchItem.__eq__
.. _JSONPatchItem.__getitem__: _modules/jsondata/jsonpatch.html#JSONPatchItem.__getitem__
.. _JSONPatchItem.__init__: _modules/jsondata/jsonpatch.html#JSONPatchItem.__init__
.. _JSONPatchItem.__ne__: _modules/jsondata/jsonpatch.html#JSONPatchItem.__ne__
.. _JSONPatchItem.__repr__: _modules/jsondata/jsonpatch.html#JSONPatchItem.__repr__
.. _JSONPatchItem.__str__: _modules/jsondata/jsonpatch.html#JSONPatchItem.__str__
.. _JSONPatchItem.apply: _modules/jsondata/jsonpatch.html#JSONPatchItem.apply
.. _JSONPatchItem.repr_export: _modules/jsondata/jsonpatch.html#JSONPatchItem.repr_export
.. _JSONPatchItem.str_export: _modules/jsondata/jsonpatch.html#JSONPatchItem.str_export
.. _JSONPatchItem: jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatchItem.__init__
.. _\__call__ (2): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatchItem.__call__
.. _\__eq__ (2): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatchItem.__eq__
.. _\__getitem__ (2): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatchItem.__getitem__
.. _\__ne__ (2): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatchItem.__ne__
.. _\__repr__ (2): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatchItem.__repr__
.. _\__str__ (2): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatchItem.__str__
.. _apply (2): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatchItem.apply
.. _repr_export (2): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatchItem.repr_export
.. _str_export (2): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatchItem.str_export


JSONPatchItemRaw
----------------
Methods
^^^^^^^
+---------------------+------------------------------+
| [docs]              | [source]                     |
+=====================+==============================+
| `JSONPatchItemRaw`_ | `JSONPatchItemRaw.__init__`_ |
+---------------------+------------------------------+

.. _JSONPatchItemRaw.__init__: _modules/jsondata/jsonpatch.html#JSONPatchItemRaw.__init__
.. _JSONPatchItemRaw: jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatchItemRaw.__init__

JSONPatchFilter
---------------
Methods
^^^^^^^
+--------------------+-----------------------------+------------------+
| [docs]             | [source]                    | [logic-operator] |
+====================+=============================+==================+
| `JSONPatchFilter`_ | `JSONPatchFilter.__init__`_ |                  |
+--------------------+-----------------------------+------------------+

Operators
^^^^^^^^^
+---------------+---------------------------+------------------+
| [docs]        | [source]                  | [logic-operator] |
+===============+===========================+==================+
| `__eq__ (4)`_ | `JSONPatchFilter.__eq__`_ | ==               |
+---------------+---------------------------+------------------+

.. _JSONPatchFilter.__init__: _modules/jsondata/jsonpatch.html#JSONPatchFilter.__init__
.. _JSONPatchFilter: jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatchFilter.__init__

.. _JSONPatchFilter.__eq__: _modules/jsondata/jsonpatch.html#JSONPatchFilter.__eq__
.. _\__eq__ (4): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatchFilter.__eq__


JSONPatch
---------

Methods
^^^^^^^
Basic
"""""
+-----------------+-----------------------+------------------+
| [docs]          | [source]              | [logic-operator] |
+=================+=======================+==================+
| `JSONPatch`_    | `JSONPatch.__init__`_ |                  |
+-----------------+-----------------------+------------------+
| `__repr__ (5)`_ | `JSONPatch.__repr__`_ | repr             |
+-----------------+-----------------------+------------------+
| `__str__ (5)`_  | `JSONPatch.__str__`_  | str              |
+-----------------+-----------------------+------------------+

Patch
"""""
+---------------------+---------------------------+------------------+
| [docs]              | [source]                  | [logic-operator] |
+=====================+===========================+==================+
| `apply (5)`_        | `JSONPatch.apply`_        |                  |
+---------------------+---------------------------+------------------+
| `get (5)`_          | `JSONPatch.get`_          |                  |
+---------------------+---------------------------+------------------+
| `patch_export (5)`_ | `JSONPatch.patch_export`_ |                  |
+---------------------+---------------------------+------------------+
| `patch_import (5)`_ | `JSONPatch.patch_import`_ |                  |
+---------------------+---------------------------+------------------+
| `repr_export (5)`_  | `JSONPatch.repr_export`_  |                  |
+---------------------+---------------------------+------------------+
| `str_export (5)`_   | `JSONPatch.str_export`_   |                  |
+---------------------+---------------------------+------------------+

Operators
^^^^^^^^^
+--------------------+--------------------------+------------------+
| [docs]             | [source]                 | [logic-operator] |
+====================+==========================+==================+
| `__add__ (5)`_     | `JSONPatch.__add__`_     | \+               |
+--------------------+--------------------------+------------------+
| `__call__ (5)`_    | `JSONPatch.__call__`_    | exec             |
+--------------------+--------------------------+------------------+
| `__eq__ (5)`_      | `JSONPatch.__eq__`_      | ==               |
+--------------------+--------------------------+------------------+
| `__getitem__ (5)`_ | `JSONPatch.__getitem__`_ | [i]              |
+--------------------+--------------------------+------------------+
| `__iadd__ (5)`_    | `JSONPatch.__iadd__`_    | +=               |
+--------------------+--------------------------+------------------+
| `__isub__ (5)`_    | `JSONPatch.__isub__`_    | -=               |
+--------------------+--------------------------+------------------+
| `__ne__ (5)`_      | `JSONPatch.__ne__`_      | !=               |
+--------------------+--------------------------+------------------+
| `__sub__ (5)`_     | `JSONPatch.__sub__`_     | \-               |
+--------------------+--------------------------+------------------+
| `__len__ (5)`_     | `JSONPatch.__len__`_     | len              |
+--------------------+--------------------------+------------------+

Iterators
^^^^^^^^^
+-----------------+-----------------------+------------------+
| [docs]          | [source]              | [logic-operator] |
+=================+=======================+==================+
| `__iter__ (5)`_ | `JSONPatch.__iter__`_ | ->               |
+-----------------+-----------------------+------------------+

.. _JSONPatch.__init__: _modules/jsondata/jsonpatch.html#JSONPatch.__init__
.. _JSONPatch: jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.__init__

.. _JSONPatch.__add__: _modules/jsondata/jsonpatch.html#JSONPatch.__add__
.. _\__add__ (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.__add__

.. _JSONPatch.__call__: _modules/jsondata/jsonpatch.html#JSONPatch.__call__
.. _\__call__ (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.__call__

.. _JSONPatch.__eq__: _modules/jsondata/jsonpatch.html#JSONPatch.__eq__
.. _\__eq__ (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.__eq__

.. _JSONPatch.__getitem__: _modules/jsondata/jsonpatch.html#JSONPatch.__getitem__
.. _\__getitem__ (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.__getitem__

.. _JSONPatch.__iadd__: _modules/jsondata/jsonpatch.html#JSONPatch.__iadd__
.. _\__iadd__ (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.__iadd__

.. _JSONPatch.__isub__: _modules/jsondata/jsonpatch.html#JSONPatch.__isub__
.. _\__isub__ (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.__isub__

.. _JSONPatch.__iter__: _modules/jsondata/jsonpatch.html#JSONPatch.__iter__
.. _\__iter__ (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.__iter__

.. _JSONPatch.__len__: _modules/jsondata/jsonpatch.html#JSONPatch.__len__
.. _\__len__ (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.__len__

.. _JSONPatch.__ne__: _modules/jsondata/jsonpatch.html#JSONPatch.__ne__
.. _\__ne__ (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.__ne__

.. _JSONPatch.__repr__: _modules/jsondata/jsonpatch.html#JSONPatch.__repr__
.. _\__repr__ (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.__repr__

.. _JSONPatch.__str__: _modules/jsondata/jsonpatch.html#JSONPatch.__str__
.. _\__str__ (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.__str__

.. _JSONPatch.__sub__: _modules/jsondata/jsonpatch.html#JSONPatch.__sub__
.. _\__sub__ (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.__sub__

.. _JSONPatch.apply: _modules/jsondata/jsonpatch.html#JSONPatch.apply
.. _apply (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.apply

.. _JSONPatch.get: _modules/jsondata/jsonpatch.html#JSONPatch.get
.. _get (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.get

.. _JSONPatch.patch_export: _modules/jsondata/jsonpatch.html#JSONPatch.patch_export
.. _patch_export (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.patch_export

.. _JSONPatch.patch_import: _modules/jsondata/jsonpatch.html#JSONPatch.patch_import
.. _patch_import (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.patch_import

.. _JSONPatch.repr_export: _modules/jsondata/jsonpatch.html#JSONPatch.repr_export
.. _repr_export (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.repr_export

.. _JSONPatch.str_export: _modules/jsondata/jsonpatch.html#JSONPatch.str_export
.. _str_export (5): jsondata_jsonpatch_doc.html#jsondata.jsonpatch.JSONPatch.str_export

.. _SCUT_JSONPOINTER:

jsondata.jsonpointer
====================
Supports *RFC6901* [RFC6901]_ and 
"Relative JSON Pointers - draft-handrews-relative-json-pointer-01" [RELPOINTER]_
.

Functions
---------

+----------------------+----------------------+------------------+
| [docs]               | [source]             | [logic-operator] |
+======================+======================+==================+
| `fetch_pointerpath`_ | `fetch_pointerpath`_ |                  |
+----------------------+----------------------+------------------+

.. _JSONPointer.fetch_pointerpath: _modules/jsondata/jsonpointer.html#fetch_pointerpath
.. _fetch_pointerpath: jsondata_jsonpointer_doc.html#fetch_pointerpath


JSONPointer
-----------

Methods
^^^^^^^

Basic
"""""
+---------------------+---------------------------------+------------------+
| [docs]              | [source]                        | [logic-operator] |
+=====================+=================================+==================+
| `JSONPointer`_      | `JSONPointer.__init__`_         |                  |
+---------------------+---------------------------------+------------------+
| `__repr__ (6)`_     | `JSONPointer.__repr__`_         | repr             |
+---------------------+---------------------------------+------------------+
| `__str__ (6)`_      | `JSONPointer.__str__`_          | str              |
+---------------------+---------------------------------+------------------+
| `isfragment`_       | `JSONPointer.isfragment`_       |                  |
+---------------------+---------------------------------+------------------+
| `isrel`_            | `JSONPointer.isrel`_            |                  |
+---------------------+---------------------------------+------------------+
| `isrelpathrequest`_ | `JSONPointer.isrelpathrequest`_ |                  |
+---------------------+---------------------------------+------------------+
| `isvalid_nodetype`_ | `JSONPointer.isvalid_nodetype`_ |                  |
+---------------------+---------------------------------+------------------+
| `isvalrequest`_     | `JSONPointer.isvalrequest`_     |                  |
+---------------------+---------------------------------+------------------+

Nodes
"""""
+--------------------------+--------------------------------------+------------------+
| [docs]                   | [source]                             | [logic-operator] |
+==========================+======================================+==================+
| `check_node_or_value`_   | `JSONPointer.check_node_or_value`_   |                  |
+--------------------------+--------------------------------------+------------------+
| `check_path_list`_       | `JSONPointer.check_path_list`_       |                  |
+--------------------------+--------------------------------------+------------------+
| `get_node`_              | `JSONPointer.get_node`_              |                  |
+--------------------------+--------------------------------------+------------------+
| `get_node_and_child`_    | `JSONPointer.get_node_and_child`_    |                  |
+--------------------------+--------------------------------------+------------------+
| `get_node_and_key`_      | `JSONPointer.get_node_and_key`_      |                  |
+--------------------------+--------------------------------------+------------------+
| `get_node_value`_        | `JSONPointer.get_node_value`_        |                  |
+--------------------------+--------------------------------------+------------------+
| `get_node_exist`_        | `JSONPointer.get_node_exist`_        |                  |
+--------------------------+--------------------------------------+------------------+
| `get_path_list`_         | `JSONPointer.get_path_list`_         |                  |
+--------------------------+--------------------------------------+------------------+
| `get_path_list_and_key`_ | `JSONPointer.get_path_list_and_key`_ |                  |
+--------------------------+--------------------------------------+------------------+
| `get_pointer`_           | `JSONPointer.get_pointer`_           |                  |
+--------------------------+--------------------------------------+------------------+
| `get_raw`_               | `JSONPointer.get_raw`_               |                  |
+--------------------------+--------------------------------------+------------------+

Operators
^^^^^^^^^
+-----------------+-------------------------+------------------+
| [docs]          | [source]                | [logic-operator] |
+=================+=========================+==================+
| `__add__ (6)`_  | `JSONPointer.__add__`_  | \+               |
+-----------------+-------------------------+------------------+
| `__call__ (6)`_ | `JSONPointer.__call__`_ | exec             |
+-----------------+-------------------------+------------------+
| `__eq__ (6)`_   | `JSONPointer.__eq__`_   | ==               |
+-----------------+-------------------------+------------------+
| `__ge__ (6)`_   | `JSONPointer.__ge__`_   | >=               |
+-----------------+-------------------------+------------------+
| `__gt__ (6)`_   | `JSONPointer.__gt__`_   | >                |
+-----------------+-------------------------+------------------+
| `__iadd__ (6)`_ | `JSONPointer.__iadd__`_ | +=               |
+-----------------+-------------------------+------------------+
| `__le__ (6)`_   | `JSONPointer.__le__`_   | <=               |
+-----------------+-------------------------+------------------+
| `__lt__ (6)`_   | `JSONPointer.__lt__`_   | <                |
+-----------------+-------------------------+------------------+
| `__ne__ (6)`_   | `JSONPointer.__ne__`_   | !=               |
+-----------------+-------------------------+------------------+
| `__radd__ (6)`_ | `JSONPointer.__radd__`_ | x+               |
+-----------------+-------------------------+------------------+

Iterators
^^^^^^^^^
+--------------------------+--------------------------------------+------------------+
| [docs]                   | [source]                             | [logic-operator] |
+==========================+======================================+==================+
| `iter_path`_             | `JSONPointer.iter_path`_             | (path)->         |
+--------------------------+--------------------------------------+------------------+
| `iter_path_nodes`_       | `JSONPointer.iter_path_nodes`_       | (path-nodes)->   |
+--------------------------+--------------------------------------+------------------+
| `iter_path_subpathdata`_ | `JSONPointer.iter_path_subpathdata`_ | (path-nodes)->   |
+--------------------------+--------------------------------------+------------------+
| `iter_path_subpaths`_    | `JSONPointer.iter_path_subpaths`_    | (path-nodes)->   |
+--------------------------+--------------------------------------+------------------+

.. _JSONPointer.isfragment: _modules/jsondata/jsonpointer.html#JSONPointer.isfragment
.. _isfragment: jsondata_jsonpointer_doc.html#isfragment

.. _JSONPointer.isrel: _modules/jsondata/jsonpointer.html#JSONPointer.isrel
.. _isrel: jsondata_jsonpointer_doc.html#isrel

.. _JSONPointer.isrelpathrequest: _modules/jsondata/jsonpointer.html#JSONPointer.isrelpathrequest
.. _isrelpathrequest: jsondata_jsonpointer_doc.html#isrelpathrequest

.. _JSONPointer.isvalid_nodetype: _modules/jsondata/jsonpointer.html#JSONPointer.isvalid_nodetype
.. _isvalid_nodetype: jsondata_jsonpointer_doc.html#isvalid-nodetype

.. _JSONPointer.isvalrequest: _modules/jsondata/jsonpointer.html#isvalrequest
.. _isvalrequest: jsondata_jsonpointer_doc.html#isvalrequest

.. _JSONPointer.iter_path_subpaths: _modules/jsondata/jsonpointer.html#JSONPointer.iter_path_subpaths
.. _iter_path_subpaths: jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.iter_path_subpaths

.. _JSONPointer.iter_path_subpathdata: _modules/jsondata/jsonpointer.html#JSONPointer.iter_path_subpathdata
.. _iter_path_subpathdata: jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.iter_path_subpathdata

.. _JSONPointer.__init__: _modules/jsondata/jsonpointer.html#JSONPointer.__init__
.. _JSONPointer: jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.__init__

.. _JSONPointer.__add__: _modules/jsondata/jsonpointer.html#JSONPointer.__add__
.. _\__add__ (6): jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.__add__

.. _JSONPointer.__call__: _modules/jsondata/jsonpointer.html#JSONPointer.__call__
.. _\__call__ (6): jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.__call__

.. _JSONPointer.__eq__: _modules/jsondata/jsonpointer.html#JSONPointer.__eq__
.. _\__eq__ (6): jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.__eq__

.. _JSONPointer.__ge__: _modules/jsondata/jsonpointer.html#JSONPointer.__ge__
.. _\__ge__ (6): jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.__ge__

.. _JSONPointer.__gt__: _modules/jsondata/jsonpointer.html#JSONPointer.__gt__
.. _\__gt__ (6): jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.__gt__

.. _JSONPointer.__iadd__: _modules/jsondata/jsonpointer.html#JSONPointer.__iadd__
.. _\__iadd__ (6): jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.__iadd__

.. _JSONPointer.__le__: _modules/jsondata/jsonpointer.html#JSONPointer.__le__
.. _\__le__ (6): jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.__le__

.. _JSONPointer.__lt__: _modules/jsondata/jsonpointer.html#JSONPointer.__lt__
.. _\__lt__ (6): jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.__lt__

.. _JSONPointer.__ne__: _modules/jsondata/jsonpointer.html#JSONPointer.__ne__
.. _\__ne__ (6): jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.__ne__

.. _JSONPointer.__radd__: _modules/jsondata/jsonpointer.html#JSONPointer.__radd__
.. _\__radd__ (6): jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.__radd__

.. _JSONPointer.__repr__: _modules/jsondata/jsonpointer.html#JSONPointer.__repr__
.. _\__repr__ (6): jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.__repr__

.. _JSONPointer.__str__: _modules/jsondata/jsonpointer.html#JSONPointer.__str__
.. _\__str__ (6): jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.__str__

.. _JSONPointer.check_node_or_value: _modules/jsondata/jsonpointer.html#JSONPointer.check_node_or_value
.. _check_node_or_value: jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.check_node_or_value

.. _JSONPointer.check_path_list: _modules/jsondata/jsonpointer.html#JSONPointer.check_path_list
.. _check_path_list: jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.check_path_list

.. _JSONPointer.get_node: _modules/jsondata/jsonpointer.html#JSONPointer.get_node
.. _get_node: jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.get_node

.. _JSONPointer.get_node_and_child: _modules/jsondata/jsonpointer.html#JSONPointer.get_node_and_child
.. _get_node_and_child: jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.get_node_and_child

.. _JSONPointer.get_node_and_key: _modules/jsondata/jsonpointer.html#JSONPointer.get_node_and_key
.. _get_node_and_key: jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.get_node_and_key

.. _JSONPointer.get_node_value: _modules/jsondata/jsonpointer.html#JSONPointer.get_node_value
.. _get_node_value: jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.get_node_value

.. _JSONPointer.get_node_exist: _modules/jsondata/jsonpointer.html#JSONPointer.get_node_exist
.. _get_node_exist: jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.get_node_exist

.. _JSONPointer.get_path_list: _modules/jsondata/jsonpointer.html#JSONPointer.get_path_list
.. _get_path_list: jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.get_path_list

.. _JSONPointer.get_path_list_and_key: _modules/jsondata/jsonpointer.html#JSONPointer.get_path_list_and_key
.. _get_path_list_and_key: jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.get_path_list_and_key

.. _JSONPointer.get_pointer: _modules/jsondata/jsonpointer.html#JSONPointer.get_pointer
.. _get_pointer: jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.get_pointer

.. _JSONPointer.get_raw: _modules/jsondata/jsonpointer.html#JSONPointer.get_raw
.. _get_raw: jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.get_raw

.. _JSONPointer.iter_path: _modules/jsondata/jsonpointer.html#JSONPointer.iter_path
.. _iter_path: jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.iter_path

.. _JSONPointer.iter_path_nodes: _modules/jsondata/jsonpointer.html#JSONPointer.iter_path_nodes
.. _iter_path_nodes: jsondata_jsonpointer_doc.html#jsondata.jsonpointer.JSONPointer.iter_path_nodes
