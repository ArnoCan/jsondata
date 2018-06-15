'jsondata.JSONTree' - Module
****************************

.. automodule:: jsondata.JSONTree

Constants
=========

Operations modes
----------------

  * _interactive = False: Activates interactive mode.

Diff Mode
---------

  * DIFF_FIRST = 0: break display of diff after first
  * DIFF_ALL = 1: list all diffs

Displayed Character Set
-----------------------

  * CHARS_RAW = 0: display character set as raw
  * CHARS_RAW = 1: display character set as str
  * CHARS_RAW = 2: display character set as utf/utf-8

Line-Overflow
-------------

  * LINE_CUT = 0: force line fit
  * LINE_WRAP = 1: wrap line in order to fit to length

JSONTree
========

.. autoclass:: JSONTree

Variables
---------

* self.difflist : reaulting differences
* self.scope: scope of differences
* self.linefit: handle overflow
* self.linewidth: line width
* self.charset: character set
* self.indent: indention steps

Methods
-------

__init__
^^^^^^^^

.. automethod:: JSONTree.__init__

printDiff
^^^^^^^^^

.. automethod:: JSONTree.printDiff

fetchDiff
^^^^^^^^^

.. automethod:: JSONTree.fetchDiff


Exceptions
==========

.. autoclass:: JSONTreeException


