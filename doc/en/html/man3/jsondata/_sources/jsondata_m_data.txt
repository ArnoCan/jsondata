'jsondata.JSONData' - Module
****************************

.. automodule:: jsondata.JSONData

Constants
=========

Compliance modes
----------------

* MODE_JSON_RFC4927 = 0: Compliant to IETF RFC4927.

* MODE_JSON_RF7951 = 2: Compliant to IETF RF7951.

* MODE_JSON_ECMA264 = 10: Compliant to ECMA-264, refer to Chapter 15.12 The JSON Object.

* MODE_POINTER_RFC6901 = 20: Compliant to IETF RFC6901.            

* MODE_PATCH_RFC6902 = 30: Compliant to IETF RFC6902.            

* MODE_SCHEMA_DRAFT3 = 43: Compliant to IETF DRAFT3.            

* MODE_SCHEMA_DRAFT4 = 44: Compliant to IETF DRAFT4.            

Types of validator
------------------

* OFF = 0: No validation.

* DRAFT4 = 1: Use draft4: jsonschema.validator(Draft4Validator)

* DRAFT3 = 2: Use draft3:jsonschema.Draft3Validator

The default value is:

* DEFAULT = *DRAFT4* = 1: Default 


Match Criteria
--------------

Match criteria for node comparison:

* MATCH_INSERT = 0: for dicts

* MATCH_NO = 1: negates the whole set

* MATCH_KEY = 2: for dicts

* MATCH_CHLDATTR = 3: for dicts and lists

* MATCH_INDEX = 4: for lists

* MATCH_MEM = 5: for dicts(value) and lists

* MATCH_NEW = 6: for the creation of new

Return Sets
-----------

* FIRST: The first match only.

* ALL: All matches.

JSONData
========
		
.. autoclass:: JSONData

Attributes
----------

* JSONData.data: JSON object data tree.

* JSONData.schema: JSONschema object data tree.


Methods
-------

__init__
^^^^^^^^

.. automethod:: JSONData.__init__


__repr__
^^^^^^^^
.. automethod:: JSONData.__repr__

__str__
^^^^^^^
.. automethod:: JSONData.__str__



branch_add
^^^^^^^^^^

.. automethod:: JSONData.branch_add

branch_copy
^^^^^^^^^^^

.. automethod:: JSONData.branch_copy

branch_create
^^^^^^^^^^^^^

.. automethod:: JSONData.branch_create

branch_move
^^^^^^^^^^^

.. automethod:: JSONData.branch_move

branch_remove
^^^^^^^^^^^^^

.. automethod:: JSONData.branch_remove

branch_replace
^^^^^^^^^^^^^^

.. automethod:: JSONData.branch_replace

branch_test
^^^^^^^^^^^

.. automethod:: JSONData.branch_test

getData
^^^^^^^

.. automethod:: JSONData.getData

getPointerPath
^^^^^^^^^^^^^^

.. automethod:: JSONData.getPointerPath

getSchema
^^^^^^^^^

.. automethod:: JSONData.getSchema

getTreeDiff
^^^^^^^^^^^

.. automethod:: JSONData.getTreeDiff

getValueNode
^^^^^^^^^^^^

.. automethod:: JSONData.getValueNode

isApplicable
^^^^^^^^^^^^

.. automethod:: JSONData.isApplicable

printData
^^^^^^^^^

.. automethod:: JSONData.printData

printSchema
^^^^^^^^^^^

.. automethod:: JSONData.printSchema

pop
^^^

.. automethod:: JSONData.pop

setSchema
^^^^^^^^^^

.. automethod:: JSONData.setSchema

validate
^^^^^^^^

.. automethod:: JSONData.validate

Operators
---------

'+'
^^^
.. automethod:: JSONData.__add__

'&&'
^^^^

.. automethod:: JSONData.__and__

'()'
^^^^

.. automethod:: JSONData.__call__


'S==x'
^^^^^^

.. automethod:: JSONData.__eq__

'[]'
^^^^

.. automethod:: JSONData.__getitem__

'S!=x'
^^^^^^

.. automethod:: JSONData.__ne__


'+='
^^^^

.. automethod:: JSONData.__iadd__

'=&&'
^^^^^

.. automethod:: JSONData.__iand__

'S%x'
^^^^^

.. automethod:: JSONData.__imod__

'*='
^^^^

.. automethod:: JSONData.__imul__

'||='
^^^^^

.. automethod:: JSONData.__ior__

'-='
^^^^

.. automethod:: JSONData.__isub__

'^='
^^^^

.. automethod:: JSONData.__ixor__

'%'
^^^

.. automethod:: JSONData.__mod__

'*'
^^^

.. automethod:: JSONData.__mul__

'||'
^^^^

.. automethod:: JSONData.__or__

'S+x'
^^^^^

.. automethod:: JSONData.__radd__

'S&&x'
^^^^^^

.. automethod:: JSONData.__rand__

'S%x'
^^^^^

.. automethod:: JSONData.__rmod__

'S*x"
^^^^^

.. automethod:: JSONData.__rmul__

'S||x"
^^^^^^

.. automethod:: JSONData.__ror__

'S^x"
^^^^^

.. automethod:: JSONData.__rxor__

'-'
^^^

.. automethod:: JSONData.__sub__

'^'
^^^

.. automethod:: JSONData.__xor__

Iterators
---------

__iter__
^^^^^^^^

.. automethod:: JSONData.__iter__

Exceptions
==========

.. autoclass:: JSONDataAmbiguity


