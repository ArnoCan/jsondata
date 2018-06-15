'jsondata.jsonpatch' - Module
*****************************
The emphasis of the design combines low resource requirement with features
designed for the application of large filters onto large JSON based data 
structures.

The patch list itself is defined by RFC6902 as a JSON array. The entries 
could be either constructed in-memory, or imported from a persistent storage.
The export feature provides for the persistent storage of a modified patch
list for later reuse.

The module contains the following classes:

* **JSONPatch**:
    The controller for the application of patches on in-memory
    data structures provided by the package 'json'.
    
* **JSONPatchItem**:
    Representation of one patch entry in accordance to RFC6902.

* **JSONPatchItemRaw**:
    Representation of one patch entry read as a raw entry in accordance to RFC6902.

* **JSONPatchFilter**:
    Selection filter for the application on the current patch list
    entries JSONPatchItem.

* **JSONDataPatchError**:
    Specific exception for this module.


The address of the the provided 'path' components for the entries are managed
by the class JSONPointer in accordance to RFC6901. 

Module
======

.. automodule:: jsondata.jsonpatch

Constansts
==========

.. index::
  pair: patch; RFC6902_ADD
  pair: patch; RFC6902_COPY
  pair: patch; RFC6902_MOVE
  pair: patch; RFC6902_REMOVE
  pair: patch; RFC6902_REPLACE
  pair: patch; RFC6902_TEST
  pair: patch; RFC6902

Operations RFC-6902
-------------------
Standard operations in accordance to RFC6902.
These are represented by the class :ref:`PATCHITEM`. 

* *RFC6902_ADD(1)* ::

     { "op": "add", "path": <rfc6901-string>, "value": <json-node> }

* *RFC6902_COPY(2)* ::

     { "op": "copy", "from": <rfc6901-string>, "path": <json-node> }

* *RFC6902_MOVE(3)* ::

     { "op": "move", "from": <rfc6901-string>, "path": <json-node> }

* *RFC6902_REMOVE(4)* ::

     { "op": "remove", "path": <rfc6901-string> }

* *RFC6902_REPLACE(5)* ::

     { "op": "replace", "path": <rfc6901-string>, "value": <json-node> }

* *RFC6902_TEST(6)* ::

     { "op": "test", "path": <rfc6901-string>, "value": <json-node> }

See :ref:`PATCHITEM`.

Functions
=========

getOp
-----

.. autofunction:: getOp


JSONPatch
=========

.. autoclass:: JSONPatch

Attributes
----------

* JSONPatch.data: JSONPatch object data tree.

Methods
-------

__init__
^^^^^^^^

.. automethod:: JSONPatch.__init__

__str__
^^^^^^^

.. automethod:: JSONPatch.__str__

                                
__repr__
^^^^^^^^

.. automethod:: JSONPatch.__repr__

apply
^^^^^

.. automethod:: JSONPatch.apply

getpatchitem
^^^^^^^^^^^^
.. automethod:: JSONPatch.getpatchitem

getpatchitems
^^^^^^^^^^^^^
.. automethod:: JSONPatch.getpatchitems

gettree
^^^^^^^
.. automethod:: JSONPatch.gettree

patch_export
^^^^^^^^^^^^

.. automethod:: JSONPatch.patch_export

patch_import
^^^^^^^^^^^^

.. automethod:: JSONPatch.patch_import

repr_export
^^^^^^^^^^^

.. automethod:: JSONPatch.repr_export

str_export
^^^^^^^^^^

.. automethod:: JSONPatch.str_export

Operators
---------

'()'
^^^^

.. automethod:: JSONPatch.__call__

'[]'
^^^^

.. automethod:: JSONPatch.__getitem__

'S+x'
^^^^^

.. automethod:: JSONPatch.__add__

'S==x'
^^^^^^

.. automethod:: JSONPatch.__eq__

'S+=x'
^^^^^^

.. automethod:: JSONPatch.__iadd__

'S-=x'
^^^^^^

.. automethod:: JSONPatch.__isub__

'S!=x'
^^^^^^

.. automethod:: JSONPatch.__ne__

'S-x'
^^^^^

.. automethod:: JSONPatch.__sub__

len
^^^

.. automethod:: JSONPatch.__len__

Iterators
---------

__iter__
^^^^^^^^

.. automethod:: JSONPatch.__iter__


.. _PATCHITEM:

JSONPatchItem
=============
.. autoclass:: JSONPatchItem

Methods
-------

__init__
^^^^^^^^

.. automethod:: JSONPatchItem.__init__

__repr__
^^^^^^^^

.. automethod:: JSONPatchItem.__repr__

__str__
^^^^^^^

.. automethod:: JSONPatchItem.__str__

apply
^^^^^

.. automethod:: JSONPatchItem.apply

repr_export
^^^^^^^^^^^

.. automethod:: JSONPatchItem.repr_export

str_export
^^^^^^^^^^

.. automethod:: JSONPatchItem.str_export

Operators
---------

'()'
^^^^

.. automethod:: JSONPatchItem.__call__

'[]'
^^^^

.. automethod:: JSONPatchItem.__getitem__

'S==x'
^^^^^^

.. automethod:: JSONPatchItem.__eq__

'S!=x'
^^^^^^

.. automethod:: JSONPatchItem.__ne__


JSONPatchItemRaw
================

.. autoclass:: JSONPatchItemRaw

Methods
-------

__init__
^^^^^^^^

.. automethod:: JSONPatchItemRaw.__init__


Class: JSONPatchFilter
======================

.. autoclass:: JSONPatchFilter

Methods
-------

__init__
^^^^^^^^

.. automethod:: JSONPatchFilter.__init__

Operators
---------

'=='
^^^^


.. automethod:: JSONPatchFilter.__eq__

'!='
^^^^

.. automethod:: JSONPatchFilter.__ne__

Exceptions
==========

.. autoexception:: JSONDataPatchError
.. autoexception:: JSONDataPatchItemError

