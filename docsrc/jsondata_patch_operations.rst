Process data by 'jsondata.jsonpatch'
************************************

The module jsondata.jsonpatch provides patch operations in 
accordance to RFC6901.


Basic types of provided basic operations are:

* **Pointer Arithmetics**:  Manipulates and calculates the pointer itself.
  Thus the comparison is related to the resulting contained set.
  Where the shorter matching pointer path contains more elements, than 
  the longer, which itself is contained in the matching shorter path. 

* **Pointed Value Evaluation**: Fetches values from JSON documents.
  Thus the comparison is related to the resulting values pointed 
  to by the pointer path.

* **Calculations with Pointed Values**: Applies common arithmetics on to evaluated 
  values and numeric parts of pointers.

Syntax Elements
===============
The current release provides the following operators for the class 'JSONPointer'.

Class Components:

* **JSONPatch**:
  Job manager for the complete set tasks represented by patch items.

* **JSONPatchItem**:
  A task in accordance to RFC6901 stored as patch item.
  The creation requires the parameters to be prepared for 
  the record format.

* **JSONPatchItemRaw**:
  Splits a raw JSON patch string into the record format
  for JSONPatchItem.

Job Manager
-----------

Job list comparison::

   ops := '==' | '!='


Add and remove task entries::

   ops := '+' | '+=' | '-' | '-='


Task execution operators::

   ops := '()' 

Miscellaneous operators::

   ops := __len__ | '[]' | '()' 

Keyword operators::

   ops := apply | get | patch_export | patch_import 


Task Items
----------

Task comparison::

   ops := '==' | '!='


Task execution operators::

   ops := '()'

Keyword operators::

   ops := apply


Examples
========

Examples for the provided basic calculations are:

Create List
-----------

* **Create a Job List**::

    jsonpatchlist = JSONPatch()


Add Item
--------
* **Add a Task Item**::

    jsonpatchlist = JSONPatch()
    for i in range(0,10):
        jsonpatchlist += JSONPatchItem("add", "/a"+unicode(i), "v"+unicode(i))


Remove Item
-----------
* **Remove a Task Item**::

    jsonpatchlist -= 8

    x = jsonpatchlist[1]
    jsonpatchlist -= x


Apply List
----------
* **Apply the Job List**::

    n,err = jsonpatchlist(configdata)
    assert n == 5
    assert err == []


Apply Item
----------
* **Apply a Task Item**::

    n,err = jsonpatchlist(configdata,0)
    ref = { "a0": "v0", "foo": "bar" }
    assert n == 1
    assert err == []
    assert ref == configdata


Export List
-----------
* **Export Job List**::

    filepath = os.path.dirname(__file__)+os.sep+"export.jsonp"
    ret = jsonpatchlist.patch_export(filepath)
    assert ret


Import List
-----------
* **Import Job List**::

    implist = JSONPatch()
    imppatch = implist.patch_import(filepath)
    assert imppatch

    assert implist == jsonpatchlist.patch
    assert implist == jsonpatchlist


