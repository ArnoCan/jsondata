Process data by 'jsondata.jsonpointer'
**************************************

The module jsondata.jsonpointer provides for the most important operators for
the assembly and evaluation of JSON pointers in accordance to RFC6901 [RFC6901]_
and the upcoming relative pointers *draft-handrews-relative-json-pointer-01* [RELPOINTER]_
.

Basic types of provided operations are:

* **Pointer Arithmetics**: 
   Manipulates and calculates the pointer itself.
   Thus the comparison is related to the resulting contained set.
   Where the shorter matching pointer path contains more elements, than 
   the longer, which itself is contained in the matching shorter path. 

* **Pointed Value Evaluation**:
   Fetches values from JSON documents.
   Thus the comparison is related to the resulting values pointed 
   to by the pointer path.

* **Calculations with Pointed Values**:
   Applies common arithmetics on to evaluated 
   values and numeric parts of pointers.

The supported categories of JSON Pointers are

+-----------------------------+---------------------+------------------------------------------------+
| type                        | pattern             | reference                                      |
+=============================+=====================+================================================+
| JSON Pointer                | '/...'              | rfc6901                                        |
+-----------------------------+---------------------+------------------------------------------------+
| JSON URI fragment           | '#/...'             | rfc6901                                        |
+-----------------------------+---------------------+------------------------------------------------+
| JSON Relative Pointer       | '<pos-integer>/...' | draft-handrews-relative-json-pointer-01 / 2018 |
+-----------------------------+---------------------+------------------------------------------------+
| JSON Relative Pointer Index | '<pos-integer>#'    | draft-handrews-relative-json-pointer-01 / 2018 |
+-----------------------------+---------------------+------------------------------------------------+

Syntax Elements
===============
The current release provides the standard absolute pointers and the newly upcoming
relative pointers.
The JSON Pointer is commonly modeled within the Python implementation as a *list* of path items. 

JSON Pointer Types
------------------
The processing of a *JSON Pointer* is supported for the combined absolute pointers within a document
in accordance to *rfc6901* [RFC6901]_ and the relative pointers in accordance to the available draft-01 [RELPOINTER]_.

|pointerevaluation|
|pointerevaluation_zoom|

.. |pointerevaluation_zoom| image:: _static/zoom.png
   :alt: zoom 
   :target: _static/pointer-evaluation.png
   :width: 16

.. |pointerevaluation| image:: _static/pointer-evaluation.png
   :width: 350

The relative pointer within a document is technically an absolute pointer within a document
mover to an starting point within the document by an relative offset. 

Absolute JSON Pointers
^^^^^^^^^^^^^^^^^^^^^^
The absolute JSON Pointers are absolute within the current scope,
actually relative to the top of the current document.
This is also the case for the supported URI fragments,
which are formally relative within the current page.
Thus it could be basically defined, that all JSON Pointers are relative,
by default with the current scope as the a fixed point of reference.

The ABNF:

.. seealso::

   RFC6901 - JSON Pointer section 3. Syntax [RFC6901]_

   A JSON Pointer is a Unicode string (see [RFC4627], Section 3)
   containing a sequence of zero or more reference tokens, each prefixed
   by a ’/’ (%x2F) character.
   Because the characters ’~’ (%x7E) and ’/’ (%x2F) have special|
   meanings in JSON Pointer, ’~’ needs to be encoded as ’~0’ and ’/’
   needs to be encoded as ’~1’ when these characters appear in a
   reference token.

   The ABNF syntax of a JSON Pointer is:

   .. code-block:: abnf
      :linenos:

      json-pointer      = *( "/" reference-token )
      reference-token   = *( unescaped / escaped )
      unescaped         = %x00-2E / %x30-7D / %x7F-10FFFF
         ; %x2F (’/’) and %x7E (’~’) are excluded from ’unescaped’
      escaped           = "~" ( "0" / "1" )
         ; representing ’~’ and ’/’, respectively

   It is an error condition if a JSON Pointer value does not conform to
   this syntax (see Section 7).
   Note that JSON Pointers are specified in characters, not as bytes.

RFC6901 compliant examples are:

.. code-block:: json
   :linenos:

   /a/b/c    # absolute path
   ''        # empty string, the whole document

The following examples are not valid, as they formally do not comply to the syntax:
   
.. code-block:: json
   :linenos:

   a/b/c    # relative path
   x        # relative path

A special variant resulting from the above syntax defintion is given by multi|ple
repetition of the slash charcater '/'

.. code-block:: python
   :linenos:

   /
   //
   ///

The *jsondata* interprets these in accordance to rfc6901 as a series of empty path items.
The example document

.. code-block:: python
   :linenos:

   x := {'': {'': {'': null}}} => p := {'': {'': {'': None}}} 

results in the following access paths and values:

+---------+---------------+------------------------+
| rfc6901 | Python        | Result                 |
+=========+===============+========================+
| ''      | p             | {'': {'': {'': None}}} |
+---------+---------------+------------------------+
| '/'     | p['']         | {'': {'': None}}       |
+---------+---------------+------------------------+
| '//'    | p['']['']     | {'': None}             |
+---------+---------------+------------------------+
| '///'   | p[''][''][''] | None                   |
+---------+---------------+------------------------+
| '#'     | p             | {'': {'': {'': None}}} |
+---------+---------------+------------------------+
| '#/'    | p['']         | {'': {'': None}}       |
+---------+---------------+------------------------+
| '#//'   | p['']['']     | {'': None}             |
+---------+---------------+------------------------+
| '#///'  | p[''][''][''] | None                   |
+---------+---------------+------------------------+

For details see [RFC6901]_ section 5 and section 6.

The specification defines the following evaluation, see [RFC6901]_ 
section "4. Evaluation":

|absolutepointerevaluation|
|absolutepointerevaluation_zoom|

.. |absolutepointerevaluation_zoom| image:: _static/zoom.png
   :alt: zoom 
   :target: _static/rfc6901-evaluation.png
   :width: 16

.. |absolutepointerevaluation| image:: _static/rfc6901-evaluation.png
   :width: 600

JSON Pointer as URI Fragments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The RFC6901 defines in addition to the pure JSON document pointers a
URI fragment syntax for the definition of JSON pointers. 

.. seealso::

   RFC6901 - section 6. URI Fragment Identifier Representation
   
   A JSON Pointer can be represented in a URI fragment identifier by
   encoding it into octets using UTF-8 [RFC3629]_, while percent-encoding
   those characters not allowed by the fragment rule in [RFC3986]_.

The syntax is quite close to the following definition of relative pointers.

Relative JSON Pointers
^^^^^^^^^^^^^^^^^^^^^^
The current draft specification 
"Relative JSON Pointers - draft-handrews-relative-json-pointer-01" [RELPOINTER]_
defines a standard syntax for the common definition of relative JSON Pointers.
The definition of a relative pointer requires two information points, the anchor
and the relative distance.

The draft standard definition combines two conceptual parts unambigously
into a single path definition:

.. code-block:: json
   :linenos:

   jsonpointer := (
      <upward-distance> <downward-distance> 
      <upward-distance> '#'
   )

   upward-distance := [1-9][0-9]*
   downward-distance := "rfc6901-path"

#. upward-distance:

   The number of steps comprising the containing arrays and objects
   in direction to the top node.

#. downward-distance:

   The number of index and key steps into the contained arrays and objects
   in direction to a leaf node.

Relative pointers provide advantage in particular within loops.

The ABNF:

.. seealso::

   draft-handrews-relative-json-pointer-01 - Relative JSON Pointers section 3. Syntax [RELPOINTER]_

   A Relative JSON Pointer is a Unicode string (see RFC 4627, 
   Section 3 [RFC4627]_ ), comprising a non-negative integer, followed by either a
   ’#’ (%x23) character or a JSON Pointer (RFC 6901 [RFC6901]_).
   The separation between the integer prefix and the JSON Pointer will
   always be unambiguous, because a JSON Pointer must be either zero-
   length or start with a ’/’ (%x2F). Similarly, a JSON Pointer will
   never be ambiguous with the ’#’.

   The ABNF syntax of a Relative JSON Pointer is:

   .. code-block:: json
      :linenos:

      relative-json-pointer  = non-negative-integer &lt;json-pointer&gt;  (*)
      relative-json-pointer  =/ non-negative-integer "#"                  (**)
      non-negative-integer   = %x30 / %x31-39 *( %x30-39 )
         ; "0", or digits without a leading "0"

   where <json-pointer> follows the production defined in RFC 6901,
   Section 3 [RFC6901]_ ("Syntax").

   **REMARK**:
      (*): This production defines a relative pointer to a resulting node.

      (**): This production evaluates the resulting location index.

The draft specification defines the following evaluation, see [RELPOINTER]_ 
section "4. Evaluation":

|relpointerevaluation|
|relpointerevaluation_zoom|

.. |relpointerevaluation_zoom| image:: _static/zoom.png
   :alt: zoom 
   :target: _static/relpointer-evaluation.png
   :width: 16

.. |relpointerevaluation| image:: _static/relpointer-evaluation.png
   :width: 700


#. Starts at a node within a document.

#. The integer value at the beginning is extracted.

   a. If the root is provided as start node, this is an error condition
   b. If the referenced value is an item within an array, then the new
      referenced value is that array.
   c. If the referenced value is an object member within an object, then
      the new referenced value is that object.

   .. note::

      **Iterpretation**: 

         The integer value is incremented as upward-moves within
         the enfolding stack of arrays and objects. The value '0'
         is the initial value itself. For example: ::

            {
               'a': {
                  'b': [
                     'c',
                     'd',
                     'e',
                  ]
               }
            }     

      With the values: ::

         start        = '/a/b/c'
         rel-pointer  = 1/2
   
      the result is: ::
   
         'e'   # 1/2 -> (1)   => bx = ['c', 'd', 'e']
               #        (1/2) => bx[2] = 'e'
   
      or with the values: ::
   
         start        = '/a/b/c'
         rel-pointer  = 3/a/b/1
   
      the result is: ::
   
         'd'   # 3/a/b/1 -> (3)       => bx               = {'a',{'b': ['c', 'd', 'e']}}
               #            (3/a)     => bx['a']          = {'b': ['c', 'd', 'e']}
               #            (3/a/b)   => bx['a']['b']     = ['c', 'd', 'e']
               #            (3/a/b/1) => bx['a']['b'][1]  = 'd'


#. If the remainder is a JSON Pointer, continue in accordance to RFC6901.

#. If the remainder is a '#'.

   a. If the root is provided as start node, this is an error condition
   b. If the referenced value is an item within an array, then the final
      evaluation result is the value’s index position within the array.
   c. If the referenced value is an object member within an object, then
      the new referenced value is the corresponding member name.

For example data refer to section "5.1 Examples" [RELPOINTER]_ :

.. code-block:: json
   :linenos:

   {
      "foo": ["bar", "baz"],
      "highly": {
         "nested": {
            "objects": true
         }
      }
   }

when starting from */foo/1* which is *baz* with the results: 

.. code-block:: json
   :linenos:

   relative path               | result   | result-type
   ----------------------------+----------+--------------
   "0"                         | "baz"    | node/value
   "1/0"                       | "bar"    | node/value
   "2/highly/nested/objects"   | true     | node/value
   "0#"                        | 1        | key/index
   "1#"                        | "foo"    | key/index

when starting from */highly/nested* which is *{"objects":true}*
with the results: 

.. code-block:: json
   :linenos:

   relative path               | result   | result-type
   ----------------------------+----------+--------------
   "0/objects"                 | true     | node/value
   "1/nested/objects"          | true     | node/value
   "2/foo/0"                   | "bar"    | node/value
   "0#"                        | "nested" | key/index
   "1#"                        | "highly" | key/index

Comparison of JSON Pointer Types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The types of JSON Pointers describe basically all the same.
A relative distance from a defined anchor.
While the absolute pointers including the URI fragment use
the top of the current document, the relative pointers provide
an offset within a given document.
The major difference is here the supported resuling upward pointer by
an integer value prefix.

+---------------------+------------------+----------------+--------+-----------+
| type                | downward pointer | upward pointer | offset | Syntax    |
+=====================+==================+================+========+===========+
| absolute            | X                | --             | --     | /a/b      |
+---------------------+------------------+----------------+--------+-----------+
| absolute-fragment   | X                | --             | --     | #/a/b     |
+---------------------+------------------+----------------+--------+-----------+
| relative node/value | X                | X              | X      | <int>/a/b |
+---------------------+------------------+----------------+--------+-----------+
| relative key/index  | --               | X              | X      | <int>#    |
+---------------------+------------------+----------------+--------+-----------+

Pointer Comparison Operators
----------------------------
Pointer comparison::

   ops := ('==' | '!=')

The comparison operators process the pointers itself, these do not verify whether an
intermediate result on the concrete JSON data iis valid or not, e.g. due to range-overflow.
The comparison in performed on the reulst of a dry-run of both pointers on a  hypothetically
ideal JSON data structure.

For example the following pointers are equal, even though maybe not applicable: ::

   offset0 = offset1 = X  # comparison allways requires equal offsets/start-modes 
   
   pointer0 = "1000/a/b"
   pointer1 = "999/b"

Behavior Operators
------------------
Pointed value evaluation operators::

   ops := '()'


Examples
========

Examples for the provided basic calculations are:

Arithmetics
-----------

* **Pointer Arithmetics**::

     import jsondata.jsonpointer

     a = JSONPointer("/a/b/c")
     b = JSONPointer("/x/y")
     c = JSONPointer("/a/b/c/2/x/y/v")
     d = JSONPointer("/a/b/c/2/x/y")
     e = JSONPointer("/a/b/c/2/x")

     # loop with increment
     for i in range(0,4):
        print str(a + i + b) + " > " + str(c) + " = " + str(a + i + b > c )

     print
     print str(a + 2 + b) + " > " + str(d) + " = " + str(a + 2 + b > d )

     print
     print str(a + 2 + b) + " > " + str(e) + " = " + str(a + 2 + b > e )

  prints the results::

     /a/b/c/0/x/y > /a/b/c/2/x/y/v = False
     /a/b/c/1/x/y > /a/b/c/2/x/y/v = False
     /a/b/c/2/x/y > /a/b/c/2/x/y/v = True
     /a/b/c/3/x/y > /a/b/c/2/x/y/v = False

     /a/b/c/2/x/y > /a/b/c/2/x/y = False

     /a/b/c/2/x/y > /a/b/c/2/x = False

  Where the shorter matching pointer path contains more elements, than 
  the longer, which itself is contained in the matching shorter path. 

Evaluation
----------

* **Pointed Value Evaluation**::

     import jsondata.jsonpointer

     jdata = { 'a': { 'b': { 'c': 2, 'd': 3 } } }

     a = JSONPointer("/a/b/c")
     b = JSONPointer("/x/y")
     c = JSONPointer("/2/x/y/v")
     d = JSONPointer("/a/b/d")

     print a(jdata) + b 
     print JSONPointer(a(jdata)) + d(jdata)
     print JSONPointer(a(jdata)) + JSONPointer(d(jdata))
     print c
     print a(jdata) + b > c

  prints the results::

     /2/x/y
     /2/3
     /2/3
     /2/x/y/v
     True 

Calculation
-----------

* **Calculations with Pointed Values**::

     import jsondata.jsonpointer

     jdata = { 'a': { 'b': { 'c': 2, 'd': 3 } } }

     a = JSONPointer("/a/b/c")
     b = JSONPointer("/x/y")
     c = JSONPointer("/2/x/y/v")
     d = JSONPointer("/a/b/d")

     print a(jdata) + d(jdata)
     print JSONPointer(a(jdata) + d(jdata))

  prints the results::

     5
     /5

