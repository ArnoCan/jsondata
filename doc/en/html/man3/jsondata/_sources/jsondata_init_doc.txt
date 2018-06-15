.. _COMMONCONSTS:

jsondata.__init__
=================
The data represented as in-memory 'json' compatible structure,
with dynamically added and/or removed branches.
The components are:

* **JSONData**:
  The main class JSONData provides for the core interface.

* **JSONDataSerializer**:
  Derived from JSONData provides for serialization and integration
  of documents and sub-documents.

* **JSONPointer**:
  The JSONPointer module provides for addressing in accordance
  to RCF7159 and RFC6901.

* **JSONPatch**:
  The JSONPatch module provides features in accordance to RFC6902.

* **JSONDiff**:
  Structure utilities.

Module
------

.. automodule:: jsondata.__init__

Constants
---------

.. index::
  pair: assign-types; C_REF
  pair: assign-types; C_DEEP
  pair: assign-types; C_SHALLOW

.. _COMMONCONSTSASSIGNTYPES:

Assigment Types
^^^^^^^^^^^^^^^
* *C_REF(0)* - OP-Copy: Copy reference.
* *C_DEEP(1)* - OP-Copy: Copy deep.
* *C_SHALLOW(2)* - OP-Copy: Copy shallow.

.. index::
  pair: op-types; B_ALL
  pair: op-types; B_AND
  pair: op-types; B_OR
  pair: op-types; B_XOR
  pair: op-types; B_MOD
  pair: op-types; B_SUB
  pair: op-types; B_MULT
  pair: op-types; B_DIV

.. _COMMONCONSTSBRANCHOPSETS:

Branch-Operations Types
^^^^^^^^^^^^^^^^^^^^^^^
* *B_ALL(0)* - OP-On-Branches: in any case.
* *B_AND(1)* - OP-On-Branches: only when both present.
* *B_OR(2)* - OP-On-Branches: if one is present.
* *B_XOR(3)* - OP-On-Branches: if only one is present.
* *B_MOD(4)* - OP-On-Branches: modulo of branches.
* *B_SUB(5)* - OP-On-Branches: subtract branches.
* *B_MULT(6)* - OP-On-Branches: add a pattern to the whole tree.
* *B_DIV(7)* - OP-On-Branches: remove a pattern from the whole tree.

.. index::
  pair: modes; CHARS_RAW
  pair: modes; CHARS_STR
  pair: modes; CHARS_UTF

.. _COMMONCONSTSCHARCTERDISP:

Character Display
^^^^^^^^^^^^^^^^^

* *CHARS_RAW(0)* - display character set as raw
* *CHARS_STR(1)* - display character set as str
* *CHARS_UTF(2)* - display character set as utf

.. index::
  pair: data-scope; SD_BOTH
  pair: data-scope; SD_INPUT
  pair: data-scope; SD_OUTPUT

.. _POINTERDISPLAYTYPE:

Data Scopes
^^^^^^^^^^^

* *SD_BOTH(0)* - Apply on mixed input and output data.

* *SD_INPUT(1)* - Apply on input data.

* *SD_OUTPUT(2)* - Apply on output data.

.. index::
  pair: pointer-display; PT_PATH
  pair: pointer-display; PT_RFC6901

.. index::
  pair: modes; PT_PATH
  pair: modes; PT_RFC6901
  pair: modes; PT_NODE

.. _COMMONCONSTSDSIPSTYLE:

Display Style
^^^^^^^^^^^^^
* *PT_PATH(0)* - Displays a list of items.
* *PT_RFC6901(1)* - Displays rfc6901 strings.
* *PT_NODE(2)* - Displays the node.


.. index::
  pair: modes; LINE_CUT
  pair: modes; LINE_WRAP

.. _COMMONCONSTSLINEOVERFLOW:

Line Handling of Overflow
^^^^^^^^^^^^^^^^^^^^^^^^^
* *LINE_CUT(0)* - force line fit
* *LINE_WRAP(1)* - wrap line in order to fit to length


.. index::
  pair: modes; MJ_RFC4627
  pair: modes; MJ_RFC7159
  pair: modes; MJ_RFC8259
  pair: modes; MJ_ECMA264
  pair: modes; MJ_RFC6901
  pair: modes; MJ_RFC6902
  pair: modes; MS_OFF
  pair: modes; MS_DRAFT3
  pair: modes; MS_DRAFT4
  pair: modes; MS_ON
  pair: modes; MODE_SCHEMA_DEFAULT

.. _COMMONCONSTSMODES:

Modes
^^^^^
Data
""""
* *MJ_RFC4627(1)* - The first JSON RFC by July 2006 [RFC4627]_.
* *MJ_RFC7493(2)* - The iJSON RFC - for now same as RFC7159 [RFC7493]_.
* *MJ_RFC7159(2)* - The JSON RFC by 'now', by March 2014 [RFC7159]_.
* *MJ_RFC8259(4)* - The JSON RFC by December 2017 [RFC8259]_.
* *MJ_ECMA264(16)* - The first JSON EMCMA standard [ECMA264]_.
* *MJ_RFC6901(32)* - JSONPointer first IETF RFC [RFC6901]_.
* *MJ_RELPOINTER(64)* - JSONPointer - relative pointer Draft-01 January 2018 [RELPOINTER]_.
* *MJ_RFC6902(128)* - JSONPatch first IETF RFC [RFC6902]_.

Schema
""""""
* *MS_DRAFT3(512)* - The first supported JSONSchema IETF-Draft.
* *MS_DRAFT4(1024)* - The current supported JSONSchema IETF-Draft [ZYP]_.

Defaults:

* *MS_ON = MS_DRAFT4* - The current default.
* *MS_OFF(0)* - No validation.
* *MODE_SCHEMA_DEFAULT = MS_OFF* - The current default validation mode.


.. index::
  pair: match-criteria; MATCH_INSERT
  pair: match-criteria; MATCH_NO
  pair: match-criteria; MATCH_KEY
  pair: match-criteria; MATCH_CHLDATTR
  pair: match-criteria; MATCH_INDEX
  pair: match-criteria; MATCH_MEM
  pair: match-criteria; MATCH_NEW
  pair: match-criteria; MATCH_PRESENT

.. _COMMONCONSTSMATCHCRITERIA:

Match Criteria
^^^^^^^^^^^^^^
Match criteria for node comparison.

* *MATCH_INSERT(0)* - For dicts.
* *MATCH_NO(1)* - Negates the whole set.
* *MATCH_KEY(2)* - For dicts.
* *MATCH_CHLDATTR(3)* - For dicts and lists.
* *MATCH_INDEX(4)* - For lists.
* *MATCH_MEM(5)* - For dicts(value) and lists.
* *MATCH_NEW(6)* - If not present create a new, else ignore and keep present untouched.
* *MATCH_PRESENT(7)* - Check all are present, else fails.

.. index::
  pair: match-sets; M_FIRST
  pair: match-sets; M_LAST
  pair: match-sets; M_ALL

.. _COMMONCONSTSMATCHSETS:

Match Sets
^^^^^^^^^^
Defines the returned sets of matches.

* *M_FIRST(1)* - The first match only.
* *M_LAST(2)* - The last match only.
* *M_ALL(4)* - All matches.


.. index::
  pair: pointer-notation; NOTATION_JSON
  pair: pointer-notation; NOTATION_HTTP_FRAGMENT

.. _COMMONCONSTSJSONNOTATION:

JSON Notation
-------------
Notation of the API - in/out.

* *NOTATION_NATIVE(0)* - JSON notation in accordance to RFC7159. This is the default.
* *NOTATION_JSON(1)* - JSON notation in accordance to RFC7159 with RFC3986.
* *NOTATION_JSON_REL(2)* - JSON notation as relative pointer.
* *NOTATION_HTTP_FRAGMENT(1)* - JSON notation in accordance to RFC7159 with RFC3986.


.. index::
  pair: scope; SC_DATA
  pair: scope; SC_SCHEMA
  pair: scope; SC_JSON
  pair: scope; SC_OBJ
  pair: scope; SC_ALL
  pair: scope; C_DEFAULT

.. _COMMONCONSTSSCOPE:

Operator Scopes
^^^^^^^^^^^^^^^
* *SC_DATA(0)* - OP-Scope: the managed JSON data only.
* *SC_SCHEMA(1)* - OP-Scope: the managed JSON schema only.
* *SC_JSON(2)* - OP-Scope: the managed JSON data and schema only.
* *SC_OBJ(3)* - OP-Scope: the attributes of current instance.
* *SC_ALL(4)* - OP-Scope: the complete object, including data.
* *C_DEFAULT = C_REF* - Default value.

.. _POINTERDISPLAYTYPE:

Pointer Display
^^^^^^^^^^^^^^^
* *PT_PATH = 0*
* *PT_RFC6901 = 1*

.. index::
  pair: print-formats; DF_SUMUP
  pair: print-formats; DF_CSV
  pair: print-formats; DF_JSON
  pair: print-formats; DF_TABLE
  pair: print-formats; DF_REVIEW
  pair: print-formats; DF_REPR
  pair: print-formats; DF_STR

.. _PRINTFORMATS:

Print Formats
^^^^^^^^^^^^^

* *DF_SUMUP = 0* - short list
* *DF_CSV = 1* - csv, for now semicolon only
* *DF_JSON = 3* - JSON struture
* *DF_TABLE = 4* - table, for now fixed
* *DF_REVIEW = 5* - short for quick review
* *DF_REPR = 6* - repr() - raw string, Python syntax
* *DF_STR = 7* - str() - formatted string, Python syntax

.. index::
  pair: return-types; R_OBJ
  pair: return-types; R_DATA
  pair: return-types; R_JDATA

.. _COMMONCONSTSRETTYPES:

Return Types
^^^^^^^^^^^^
* *R_OBJ(0)* - Return object of type self.
* *R_DATA(1)* - Return self.data.
* *R_JDATA(2)* 0 Return object of type JSONData.

.. index::
  pair: sort-order; SEARCH_FIRST
  pair: sort-order; SEARCH_ALL

.. _SEARCHPARAM:

Search Parameters
^^^^^^^^^^^^^^^^^
* *SEARCH_FIRST(0)* - Break display after first match.
* *SEARCH_ALL(1)* - List all matches.


.. index::
  pair: sort-order; S_NONE
  pair: sort-order; S_SIMPLE

.. _SORTORDER:

Sort Order
^^^^^^^^^^
* *S_NONE = 0* - no sort
* *S_SIMPLE = 1* - goups upper lower


Exceptions
----------

.. autoexception:: JSONDataAmbiguityError
.. autoexception:: JSONDataDiffError
.. autoexception:: JSONDataError
.. autoexception:: JSONDataIndexError
.. autoexception:: JSONDataKeyError
.. autoexception:: JSONDataModeError
.. autoexception:: JSONDataNodeTypeError
.. autoexception:: JSONDataParameterError
.. autoexception:: JSONDataPatchError
.. autoexception:: JSONDataPatchItemError
.. autoexception:: JSONDataPathError
.. autoexception:: JSONDataPointerError
.. autoexception:: JSONDataPointerTypeError
.. autoexception:: JSONDataSearchError
.. autoexception:: JSONDataSourceFileError
.. autoexception:: JSONDataTargetFileError
.. autoexception:: JSONDataTypeError
.. autoexception:: JSONDataValueError
.. autoexception:: JSONPointerError
