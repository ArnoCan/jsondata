'jsondata.JSONPatch' - Module
******************************

.. automodule:: jsondata.JSONPatch

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

get
^^^
.. automethod:: JSONPatch.get

patch_export
^^^^^^^^^^^^

.. automethod:: JSONPatch.patch_export

patch_import
^^^^^^^^^^^^

.. automethod:: JSONPatch.patch_import

repr_export
^^^^^^^^^^^

.. automethod:: JSONPatch.repr_export

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
^^^^^^^^^

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

* `jsondata.JSONPatchException [source] <_modules/jsondata/JSONPatch.html#JSONPatchException>`_

* `jsondata.JSONPatchItemException [source] <_modules/jsondata/JSONPatch.html#JSONPatchItemException>`_


