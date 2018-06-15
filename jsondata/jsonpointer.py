# -*- coding:utf-8   -*-
"""Provides classes for the JSONPointer definition in
accordance to RFC6901 and relative pointers draft-1/2018.
"""
from __future__ import absolute_import
from __future__ import print_function

import re
import copy

from jsondata import V3K, ISSTR, JSONPointerError, JSONPointerTypeError, \
    C_SHALLOW, C_DEEP, \
    M_FIRST, M_LAST, \
    rtypes2num, RT_LST, RT_JSONPOINTER, \
    verify2num, V_FINAL, V_STEPS


__author__ = 'Arno-Can Uestuensoez'
__maintainer__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez" \
                " @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.21'
__uuid__ = '63b597d6-4ada-4880-9f99-f5e0961351fb'

if V3K:
    unicode = str
    from urllib.parse import unquote as url_unquote  # @UnresolvedImport @UnusedImport pylint: disable=import-error
else:
    from urllib import unquote as url_unquote  # @UnresolvedImport  @Reimport pylint: disable=import-error

# Sets display for inetractive JSON/JSONschema design.
_interactive = False

from jsondata import NOTATION_JSON, NOTATION_JSON_REL, NOTATION_HTTP_FRAGMENT

VALID_NODE_TYPE = (
    dict,
    list,
    str,
    unicode,
    int,
    float,
    bool,
    None,
    )  #: Valid types of in-memory JSON node types.

CHARSET_UTF = 0  #: Unicode.
CHARSET_STR = 1  #: Python string.

#
# relative JSON Pointer - [RELPOINTER] draft-handrews-relative-json-pointer-01
#
# 1: integer offset
#    and 3:  fetch key
#    and 4:  fetch node @relpath
#    and 5:  offset only - top document
#
# else: error
#
if V3K:
    _RELPOINTER = re.compile(r"(0|[1-9][0-9]*)(([#]$)|(/.*$)|($))")  # 1 +(3 | 4 | 5)
else:
    _RELPOINTER = re.compile(unicode(r"(0|[1-9][0-9]*)(([#]$)|(/.*$)|($))"))  # 1 +(3 | 4 | 5)

#: Unescaped character in reference-token [RFC6901]_
_unescaped = re.compile(r'/|~[^01]')


_privattr = {
    'isfragment': '__isfragment',
    'isrel': '__isrel',
    'raw': '__raw',
    'relupidx': '__relupidx',
    'start': '__start',
    'startrel': '__startrel',
} #: private attributes accessible by __steattr__ and __getattr__ only


def fetch_pointerpath(node, base, restype=M_FIRST):
    """Converts the address of *node* within the data structure
    *base* into a corresponding pointer path.
    The current implementation is search based, thus
    may cause performance issues when frequently applied,
    or processing very large structures.

    For example: ::

       nodex = {'a': 'pattern'}
       data = {0: nodex, 1: [{'x':[nodex}]]}

       res = fetch_pointerpath(nodex, data)

       res = [
          [0],
          [1, 0, 'x', 0]
       ]

    Args:

        **node**:
            Address of Node to be searched for.

        **base**:
            A tree top node to search the subtree for node.

        **restype**:
            Type of search. ::

               M_FIRST: The first match only.
               M_LAST: The first match only.
               M_ALL: All matches.

    Returns:

        Returns a list of lists, where the contained
        lists are pointer pathlists for matched elements.

        * restype:=M_FIRST: '[[<first-match>]]',

        * restype:=M_LAST: '[[<last-match>]]',

        * restype:=M_ALL: '[[<first-match>],[<second-match>],...]'

    Raises:

        JSONDataError

    """
    if not node or not base:
        return []

    if isinstance(base, JSONData):
        base = base.data

    spath = []
    res = []

    kl = 0

    if type(base) is list:  # first layer - list of elements
        kl = 0
        if id(node) == id(base):  # top node
            res.append([kl])
        else:
            for sx in base:
                if id(node) == id(sx):
                    s = spath[:]
                    s.append(kl)
                    res.append(s)

                elif type(sx) in (dict, list):
                    sublst = fetch_pointerpath(node, sx, restype)
                    if sublst:
                        for slx in sublst:
                            # TODO: update the documentation-scanner: res.append([kl, *slx])
                            _l = [kl]
                            _l.extend(slx)
                            res.append(_l)
                elif type(sx) in (tuple, set,):
                    raise JSONPointerError(sx)
                kl += 1

    elif type(base) is dict:  # first layer - dict of elements
        if id(node) == id(base):  # top node
            res.append([''])
        else:
            for k, v in base.items():
                if id(node) == id(v):
                    spath.append(k)
                    res.append(spath)
                    continue
                elif type(v) in (list, dict):
                    sublst = fetch_pointerpath(node, v, restype)
                    if sublst:
                        for slx in sublst:
                            if slx:
                                # TODO: update the documentation-scanner: res.append([k, *slx])
                                _l = [k]
                                _l.extend(slx)
                                res.append(_l)
                elif type(v) in (tuple, set,):
                    raise JSONPointerError(v)

    elif type(base) in (tuple, set,):
        raise JSONPointerError(base)

    if res and restype == M_FIRST:
        return [res[0]]
    elif res and restype == M_LAST:
        return [res[-1]]
    return res


class JSONPointer(list):
    """Represents exactly one JSONPointer in compliance with
    IETF RFC6901 and relative-pointer/draft-1/2018
    """
    VALID_INDEX = re.compile('0|[1-9][0-9]*$')
    """Regular expression for valid numerical index."""

    def __init__(self, ptr, **kargs):
        """Normalizes and stores a JSONPointer. The internal
        representation depends on the type.

        * absolute path:

          A list of ordered items representing
          the path items.

        * relative path:

          Relative paths in addition provide
          a positive numeric offset of outer
          containers [RELPOINTER]_.

        Processes the ABNF of a JSON Pointer from RFC6901
        and/or a relative JSON Pointer(draft 2018).

        Attributes:
            For details see manuals.

            * *isfragment*
            * *isrel*
            * *raw*
            * *start*
            * *startrel*

        Args:
            **ptr**:
                A JSONPointer to be represented by this object. The
                supported formats are:

                .. parsed-literal::

                   ptr := (
                       JSONPointer                  # [RFC6901]_ or [RELPOINTER]_
                       | <rfc6901-string>           # [RFC6901]_
                       | <relative-pointer-string>  # [RELPOINTER]_
                       | <pointer-items-list>       # non-URI-fragment pointer path items of [RFC6901]_
                       )

                JSONPointer:
                    A valid object, is copied into this object,
                    see 'deep'. Supports *rfc6901* [RFC6901]_
                    and *relative* pointers [RELPOINTER]_.

                *rfc6901-string*:
                    A string i accordance to RFC6901 [RFC6901]_.

                *relative-pointer-string*:
                    Draft standard, currently
                    experimental [RELPOINTER]_.

                *pointer-items-list*:
                    Expects a path list, where each item
                    is processed for escape and unquote.
                    Supports *rfc6901* pointers [RFC6901]_.

                Containing:

                * absolute JSON Pointer
                * relative JSON Pointer, requires the
                  keyword argument *startrel*

            kargs:

                **debug**:
                    Enable debugging.

                **deep**:
                    Applies for copy operations on structured data
                    'deep' when 'True', else 'shallow' only.
                    Flat data types are copied by value in any case.

                **node**:
                    Force to set the pointed node in the internal cache.

                **replace**:
                    Replace masked characters, is applied onto the *ptr*
                    parameter only. For the replacement of *startrel*
                    create and pass an object *JSONPointer*. ::

                       replace := (
                            True    # replaces rfc6901 escape sequences: ~0 and ~1
                          | False   # omit unescaping
                       )

                    .. note::

                       Match operations on address strings are proceeded literally,
                       thus the escaped characters should be consistent,
                       see rfc6901, Section 3.

                    default := False

                **startrel**:
                    Start node for relative JSON Pointers. Is evaluated
                    only in combination with a relative path, else
                    ignored. ::

                       startrel := (
                            JSONPointer           # supports [RFC6901]_ and [RELPOINTER]_
                          | <rfc6901-string>      # supports [RFC6901]_
                          | <rel-pointer-string>  # supports only relative to whole-document '0/...'
                       )

                    default := ""  # whole document

        Returns:
            When successful returns *True*, else returns either *False*, or
            raises an exception.
            Success is the complete addition only, thus one failure returns
            *False*.

        Raises:
            JSONPointerError:

        """

        self.debug = kargs.get('debug', False)
        self.deep = deep = kargs.get('deep', False)
        self.node = kargs.get('node', None)  # cache for reuse
        self.__startrel = kargs.get('startrel', '')  # default whole document
        replace = kargs.get('replace', False)

        super(JSONPointer, self).__init__()

        if type(ptr) in (int, float):  # pointer are unicode only
            ptr = unicode(ptr)  # is relative pointer
            self.__raw = ptr

        elif deep:
            if type(ptr) in ISSTR:
                self.__raw = ptr[:]
            else:
                self.__raw = copy.deepcopy(ptr)
        else:
            if type(ptr) in ISSTR:
                self.__raw = ptr
            elif isinstance(ptr, JSONPointer):
                self.__raw = JSONPointer(ptr.get_raw(), startrel=ptr.get_startrel())
            else:
                self.__raw = copy.copy(ptr)

        self.__isrel = False  #: marks a relative pointer
        self.__start = None
        self.__isfragment = False  #: marks a uri fragment

        if type(ptr) in (list, tuple):  # no-fragment rfc6901
            self.extend(ptr)
            return

        if ptr in('', '#'):  # shortcut for whole document, see RFC6901
            # '#' is URI fragments RFC6901 section 6
            return None

        elif ptr == '/':  # shortcut for empty tag at top-level, see RFC6901
            self.append('')
            return None

        elif isinstance(ptr, ISSTR):  # string in accordance to RFC6901
            if ptr == '#/':  # URI fragments RFC6901 section 6
                self.__isfragment = True
                self.append('')
                return None

            elif ptr.startswith('#'):  # URI fragments RFC6901 section 6
                self.__isfragment = True
                ptr = url_unquote(ptr[1:])

            elif ptr[0].isdigit():  # relative pointer - 2018/draft1 see doc [RELPOINTER]

                #
                # 1: integer offset
                # 3: fetch key
                # 4: fetch node @relpath
                # 5: int
                #
                _m = _RELPOINTER.match(ptr)
                if _m is None:
                    raise JSONPointerError("Syntax:" + str(ptr))
                self.__isrel = True

                if type(self.__startrel) not in (JSONPointer, list, str, unicode):
                    _sr = str(type(self.__startrel)) + " / " + str(self.__startrel)
                    if len(_sr) >200:
                        _sr = _sr[:200]
                    raise JSONPointerError("type not supported startrel=" + _sr)

                #
                # <int><jsonpointer> or <int>#
                #
                self.__relupidx = int(_m.group(1))  # <int> - upward increment
                if self.__relupidx == None:
                    raise JSONPointerError("Cannot scan:" + str(ptr))

                if _m.group(4):  # <int><jsonpointer>
                    ptr = _m.group(4)  # downward path
                    self.__isrelpathrequest = True

                elif _m.group(3):  # fetch-key/fetch-index
                    ptr = None
                    self.__isrelpathrequest = False

                elif _m.group(5) != None:  # <int> - whole rel-sub-document
                    ptr = None
                    self.__isrelpathrequest = True
                else:
                    raise JSONPointerError("Cannot scan:" + str(ptr))

                if type(self.__startrel) in ISSTR or type(self.__startrel) is list:
                    self.__startrel = JSONPointer(self.__startrel)

                if len(self.__startrel) < self.__relupidx: # integer prefix-overflow
                    raise JSONPointerError(
                        "\ninteger prefix overflow:"
                        + "\n prefix        = " + str(self.__relupidx)
                        + "\n len(startrel) = " + str(len(self.__startrel))
                        + "\n startrel      = " + str(self.__startrel)
                        )

                elif len(self.__startrel) == self.__relupidx:  # integer-prefix equel to offset
                    if self.__isrelpathrequest:  # anchor for a relative path
                        self.__start =  JSONPointer(self.__startrel[:(len(self.__startrel)-self.__relupidx)])
                    else:  # request for key/index
                        raise JSONPointerError(
                            "\nkey/index request for <whole-document> prohibited by specification [RELPOINTER], see manuals:"
                            + "\n prefix        = " + str(self.__relupidx)
                            + "\n len(startrel) = " + str(len(self.__startrel))
                            + "\n startrel      = " + str(self.__startrel)
                            )


                elif len(self.__startrel) > self.__relupidx:  # integer-prefix within offset
                    self.__start =  JSONPointer(self.__startrel[:(len(self.__startrel)-self.__relupidx)])

                else:
                    self.__start =  JSONPointer('')

            if ptr is not None:
                self.extend(ptr.split('/'))

                if len(self) == 1 or self[0] != '':
                    raise JSONPointerTypeError("requires a valid JSON pointer: " + str(ptr))

                self.pop(0)

        elif isinstance(ptr, JSONPointer):  # copy constructor
            if ptr.isrel():
                self.__isrel = ptr.isrel()
                self.__relupidx = ptr.get_relupidx()
                self.__isrelpathrequest = ptr.isrelpathrequest()

            if deep:
                self.__raw = ptr.get_raw()[:]
                if ptr.isrel():
                    self.__start = ptr.get_start().copy()
                    self.__startrel = ptr.get_startrel().copy()
                self.extend(ptr.copy_path())
            else:
                self.__raw = ptr.get_raw()
                if ptr.isrel():
                    self.__start = ptr.get_start().copy()
                    self.__startrel = ptr.get_startrel().copy()
                self.extend(ptr)

        elif type(ptr) is list:
            # list of entries in accordance to RFC6901, and JSONPointer

            def presolv(p0):
                if isinstance(p0, JSONPointer):  # copy constructor
                    return p0.ptr
                elif p0 in ('', '/'):
                    return p0
                elif type(p0) in (str, unicode):
                    return p0
                elif type(p0) in (int, float):
                    return str(p0)
                else:
                    raise JSONPointerError("Invalid nodepart:" + str(p0))
                return p0

            if deep:
                self.extend(map(lambda s: s[:], ptr))
            else:
                self.extend(map(presolv, ptr))
            self.__raw = '/' + '/'.join(self)

        else:
            if not ptr:
                self.__raw = None
                return None
            raise JSONPointerError("Pointer type not supported:",
                                       type(ptr))

        def _rep0(x):
            if type(x) in (str, unicode):
                if x.isdigit():
                    return int(x)
                return url_unquote(x).replace('~1', '/').replace('~0', '~')
            return x

        def _rep1(x):
            if type(x) in (str, unicode):
                if x.isdigit():
                    return int(x)
            return x

        if replace:
            sx = [_rep0(x) for x in self]
        else:
            sx = [_rep1(x) for x in self]

        del self[:]
        self.extend(sx)

    def __add__(self, x):
        """Appends a Pointer to self.

        Args:
            **x**:
                A valid JSONPointer of type: ::

                   x := (
                      JSONPointer - fragment
                      | JSONPointer - relative-pointer
                      | relative pointer
                      )

        Returns:
            A new object of JSONPointer

        Raises:
            JSONPointerError:

        """
        ret = JSONPointer(self)
        # pointer are unicode only, RFC6901/RFC3829
        try:
            if type(x) in (str, unicode) and x[0] is '#':
                x = x[1:]
        except IndexError:
            pass

        if x == '':  # whole document, RFC6901
            pass
        elif x == u'/':  # empty tag
            ret.__raw += x
            ret.append('')
        elif isinstance(x, JSONPointer):
            ret.__raw += x.raw
            ret.extend(x)
        elif type(x) in (list, tuple,):
            ret.__raw += u'/' + u'/'.join(x)
            ret.extend(x)
        elif type(x) in (str, unicode):
            if x[0] == u'/':
                ret.extend(x[1:].split('/'))
                ret.__raw += x
            else:
                ret.extend(x.split('/'))
                ret.__raw += u'/' + x
        elif type(x) is int:
            ret.append(x)
            ret.__raw += u'/' + unicode(x)
        elif x  is None:
            return ret

        else:
            raise JSONPointerError()
        return ret

    def __call__(self, x, *args, **kargs):
        """Evaluates the pointer value on the document.

        Args:
            **x**:
                A valid JSON document.

        Returns:
            The resulting pointer value.

        Raises:
            JSONPointerError
        """
        return self.evaluate(x, *args, **kargs)

    def __delattr__(self, name):
        raise NotImplementedError("delete: " + name)

    def __eq__(self, x):
        """Compares this pointer with x.

        Args:
            **x**:
                A JSONPointer object.

        Returns:
            True or False

        Raises:
            JSONPointerError
        """
        if isinstance(x, JSONPointer):
            return self.get_pointer_str(NOTATION_JSON) == x.get_pointer_str(NOTATION_JSON)
        elif type(x) == list:
            if not x:
                return self.get_pointer_str(NOTATION_JSON) == u''
            return self.get_pointer_str(NOTATION_JSON) == u'/' + u'/'.join(map(unicode, x))
        elif type(x) in (str, unicode):
            return self.get_pointer_str(forcenotation=NOTATION_JSON) == x
        elif type(x) is int:
            return self.get_pointer_str(forcenotation=NOTATION_JSON) == u'/' + unicode(x)
        elif x  is None:
            return False
        else:
            raise JSONPointerError()
        return False

    def __ge__(self, x):
        """Checks containment(>=) of another pointer within this.

        The weight of contained entries is the criteria, though
        the shorter is the bigger. This is true only in case of
        a containment relation.

        The number of equal path pointer items is compared.

        Args:
            **x**:
                A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerError:

        """
        if isinstance(x, JSONPointer):
            return super(JSONPointer, self).__le__(x)
        elif type(x) in ISSTR:
            return super(JSONPointer, self).__le__(JSONPointer(x))
        else:
            raise JSONPointerError()

    def __gt__(self, x):
        """Checks containment(>) of another pointer or object within this.

        The number of equal items is compared.

        Args:
            **x**:
                A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerError:
        """
        if isinstance(x, JSONPointer):
            return super(JSONPointer, self).__gt__(x)
        elif type(x) in ISSTR:
            return super(JSONPointer, self).__lt__(JSONPointer(x))
        else:
            raise JSONPointerError()

    def __iadd__(self, x):
        """Add in place x to self, appends a path.

        Args:
            **x**:
                A valid Pointer.

        Returns:
            'self' with updated pointer attributes

        Raises:
            JSONPointerError:
        """
        if type(x) == list:
            self.__raw += unicode('/' + '/'.join(x))
            self.extend(x)
        elif isinstance(x, JSONPointer):
            if x.raw[0] != u'/':
                self.__raw += u'/' + x.raw
            else:
                self.__raw = x.raw
            self.extend(x)
        elif type(x) is int:
            self.append(unicode(x))
            self.__raw += u'/' + unicode(x)
        elif x == '':  # whole document, RFC6901
            raise JSONPointerError("Cannot add the whole document")
        elif x == u'/':  # empty tag
            self.__raw += x
            self.append('')
        elif type(x) in (str, unicode):
            if x[0] == u'/':
                self.extend(x[1:].split('/'))
                self.__raw += x
            else:
                self.extend(x.split('/'))
                self.__raw += u'/' + x
        elif x  is None:
            return self

        else:
            raise JSONPointerError()
        return self

    def __le__(self, x):
        """Checks containment(<=) of this pointer within another.

        The number of equal items is compared.

        Args:
            **x**:
                A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerError:
        """
        if isinstance(x, JSONPointer):
            return super(JSONPointer, self).__ge__(x)
        elif type(x) in ISSTR:
            return super(JSONPointer, self).__ge__(JSONPointer(x))
        else:
            raise JSONPointerError()

    def __lt__(self, x):
        """Checks containment(<) of this pointer within another.

        The number of equal items is compared.

        Args:
            **x**:
                A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerError:
        """
        if isinstance(x, JSONPointer):
            return super(JSONPointer, self).__gt__(x)
        elif type(x) in ISSTR:
            return super(JSONPointer, self).__gt__(JSONPointer(x))
        else:
            raise JSONPointerError()

    def __ne__(self, x):
        """Compares this pointer with x.

        Args:
            **x**:
                A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerError
        """
        return not self.__eq__(x)

    def __radd__(self, x):
        """Adds itself as the right-side-argument to the left.

        This method appends 'self' to a path fragment on the left.
        Therefore it adds the path separator on it's left side only.
        The left side path fragment has to maintain to be in
        accordance to RFC6901 by itself.

        Once 'self' is added to the left side, it terminates it's
        life cycle. Thus another simultaneous add operation is
        handled by the resulting other element.

        Args:
            **x**:
                A valid Pointer.

        Returns:
            The updated input of type 'x' as 'x+S(x)'

        Raises:
            JSONPointerError:
        """
        if x == '':  # whole document, RFC6901
            return u'/' + u'/'.join(map(unicode, self))
        elif x == u'/':  # empty tag
            return x + u'/' + u'/'.join(map(unicode, self))
        elif type(x) is int:
            return u'/' + unicode(x) + u'/' + u'/'.join(map(unicode, self))
        elif type(x) in (str, unicode):
            return x + u'/' + u'/'.join(map(unicode, self))
        elif type(x) == list:
            return x.extend(self)
        else:
            raise JSONPointerError()
        return x

    def __repr__(self):
        """Returns the attribute self.__raw, which is the raw input JSONPointer.

        Args:
            None

        Attributes:
            Evaluates *self.__isrel*

        Returns:
            For relative paths: ::
               (<start-offset>, <pointer>)

               start-offset := [<self.startrel>]
               pointer := [<self>]

            For RFC6901 paths: ::

               <pointer>

               pointer := [<self>]

        Raises:
            pass-through

        """
        if self.__isrel:
            ret = '(%s, %s)' % (
                repr(self.__start),
                unicode(super(JSONPointer, self).__repr__()),
                )

        else:
            ret = super(JSONPointer, self).__repr__()

        if ret == '':
            return "''"
        return ret

    def __setattr__(self, name, value):
        try:
            self.__dict__[_privattr[name]] = value
        except KeyError:
            self.__dict__[name] = value

    def __str__(self):
        """Returns the string for the processed path.

        Args:
            None

        Attributes:
            Evaluates *self.__isrel*

        Returns:
            For relative paths: ::
               (<start-offset>, <pointer>)

               start-offset := [<self.startrel>]
               pointer := [<self>]

            For RFC6901 paths: ::

               <pointer>

               pointer := [<self>]

        Raises:
            pass-through

        """

        if self.__isrel:
            if self.__start:
                ret = "%s" % (
                    '/' + '/'.join((str(x) for x in self.__start)) + '/' + '/'.join((str(x) for x in self))
                    )
            elif self:
                ret = "%s" % ('/' + '/'.join((str(x) for x in self)))
            else:
                ret = '""'

        else:
            if self:
                ret = "%s" % ('/' + '/'.join((str(x) for x in self)))
            else:
                ret = '""'

        if ret == '':
            return "''"
        return ret

    def check_node_or_value(self, jsondata, parent=False):
        """Checks the existence of the corresponding node
        within the JSON document.

        Args:
            **jsondata**:
                A valid JSON data node.

            **parent**:
                If *True* returns the parent node of the pointed value.

        Returns:
            True or False

        Raises:
            JSONPointerError:

            pass-through
        """
        if self == []:  # special RFC6901, whole document
            return not (not jsondata)
        elif self == ['']:  # special RFC6901, '/' empty top-tag
            try:
                return not ( not jsondata[''])
            except KeyError:
                return False

        if not self.isvalid_nodetype(jsondata):
            # concrete info for debugging for type mismatch
            raise JSONPointerError("Invalid nodetype parameter:" +
                                       str(type(jsondata)))

        if parent:
            _s = self[:-1]
        else:
            _s = self
        for x in _s:
            if isinstance(jsondata, dict):
                jsondata = jsondata.get(x, False)
                if not jsondata:
                    return False
            elif isinstance(jsondata, list):
                jsondata = jsondata[x]
                if not jsondata:
                    return False

        if not self.isvalid_nodetype(jsondata):
            # concrete info for debugging for type mismatch
            raise JSONPointerError("Invalid path nodetype:" +
                                       str(type(jsondata)))
        self.node = jsondata  # cache for reuse
        return True

    def copy(self, **kargs):
        """Creates a copy of self.

        Args:
            None

            kargs:
                **deep**:
                    When *True* creates a deep copy,
                    else shallow.

        Returns:
            A copy of self.

        Raises:
            pass-through
        """
        return JSONPointer(self, copydata=kargs.get('deep', C_DEEP))

    def copy_path_list(self, parent=False):
        """Returns a deep copy of the objects pointer path list.

        Args:
            **parent**:
                The parent node of the pointer path.

        Returns:
            A copy of the path list.

        Raises:
            none
        """
        if self == []:  # special RFC6901, whole document
            return []
        if self == ['']:  # special RFC6901, '/' empty top-tag
            return ['']

        if parent:
            return [ s[:] for s in self[:-1]]
        else:
            return [ s[:] for s in self[:]]

#         if parent:
#             return map(lambda s: s[:], self[:-1])
#         else:
#             return map(lambda s: s[:], self[:])

    def __deepcopy__(self, memo):
        # return JSONPointer(self[:], copydata=C_DEEP)
        return JSONPointer(self[:])
    
    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError as e:
            if V3K:
                raise JSONPointerError(
                    "Unknown attribute: " + repr(e)
                    ) # from None
            else:
                raise JSONPointerError(
                    "Unknown attribute: " + repr(e)
                    )

    def get_key(self):
        """Get the resulting key for the pointer. In case
        of a relative pointer as resulting from the processing
        of the relative pointer and the starting node.
        """
        if not self.__isrel:  # pointer in accordance to rfc6901
            if self == None:
                # data is not initialized at all - basically impossible - anyhow
                return None

            elif not self:
                # whole document - RFC6901
                return ''

            return self[-1]

        #
        # relative draft-1/2018
        #
        if self.__isrelpathrequest:  # is get relpath request
            if not self:  # special - whole rel document - integer only
                if not self.__start:  # no offset
                    return None
                return str(self.__start[-1])  # resulting offset only
            return self[-1]  # a valid pointer

        else:  # is get-key/index - request
            # self is None in any case
            if not self.__start:  # the whole document
                return None

            elif len(self.__start) - 1 - self.__relupidx <= 0:  # the whole document - fs-like for index-overflow
                return None

            return str(self.__start[len(self.__start) - 1 - self.__relupidx])

    def get_node_and_child(self, jsondata):
        """Returns a tuple containing the parent node and self as the child.

        Args:
            **jsondata**:
                A valid JSON data node.

        Returns:
            The the tuple: ::

               (p, c):
                  p: Node reference to parent container.
                  c: Node reference to self as the child.

        Raises:
            JSONPointerError:

            pass=through
        """
        n = self(jsondata, True) # get parent
        if len(self) == 1:
            return n, None
        try:
            return n, self(jsondata, False)
        except (IndexError, KeyError):
            return n, None
        raise JSONPointerError(self.__raw)

    def get_node_and_key(self, jsondata):
        """Returns a tuple containing the parent node and the key of current.

        Args:
            **jsondata**:
                A valid JSON data node.

        Returns:
            The the tuple: ::

               (n, k):
                  n: Node reference to parent container.
                  k: Key for self as the child entry:

                     k := (
                          <list-index>
                        | <dict-key>
                        | None
                     )

                     list-index: 'int'
                     dict-key: 'UTF-8'
                     None: "for root-node"

        Raises:
            JSONPointerError:

            pass-through
        """
        n = self(jsondata, True)
        if len(self) == 1 and self[0] == '':
            return n, None

        try:
            return n, self[-1],
        except (IndexError, KeyError):
            return n, None
        raise JSONPointerError(self.__raw)

    def get_node_value(self, jsondata, cp=C_SHALLOW, **kargs):
        """Gets the copy of the corresponding node.
        Relies on the standard package 'json'.

        Args:
            **jsondata**:
                A valid JSON data node.

            **cp**:
                Type of returned copy. ::

                   cp := (
                        C_DEEP
                      | C_REF
                      | C_SHALLOW
                   )

            kargs:
                **valtype**:
                    Type of requested value.

        Returns:
            The copy of the node, see option *copy*.

        Raises:
            JSONPointerError

            pass-through
        """
        valtype = kargs.get('valtype', None)

        _resroot = self.get_pointer(jsondata, superpose=True)
        if _resroot == None:  # basically impossible - anyhow
            return None
        if not _resroot:  # == [] : special RFC6901, whole document
            return jsondata
        elif len(_resroot) == 0:
            return jsondata  # same as previous
        elif len(_resroot) == 1:
            if _resroot[0] == '':
                return jsondata  # the whole document
            try:
                return jsondata[_resroot[0]]  #
            except (KeyError, IndexError) as e:
                if V3K:
                    raise JSONPointerError(
                        "Node(" + str(self.index(0)) + "):" + str(self[0]) + " of " + str(self) + ":" + str(e)
                        #
                        # TODO: update doctool for python3 introspection
                        #
                        ) # from None
                else:
                    raise JSONPointerError(
                        "Node(" + str(self.index(0)) + "):" + str(self[0]) + " of " + str(self) + ":" + str(e)
                        )

        if not self.isvalid_nodetype(jsondata):
            raise JSONPointerError("Invalid nodetype parameter:" +
                                       str(type(jsondata)))

        try:
            for x in _resroot:
                if not isinstance(jsondata, (list, dict, JSONData)):
                    break
                try:
                    jsondata = jsondata[x]  # want the exception
                except TypeError:
                    jsondata = jsondata[int(x)]  # still want the exception

        except Exception as e:
            if V3K:
                raise JSONPointerError(
                    "Node(" + str(self.index(x)) + "):" + str(x) + " of " + str(self) + ":" + str(e)
                        #
                        # TODO: update doctool for python3 introspection
                        #
                    ) # from None
            else:
                raise JSONPointerError(
                    "Node(" + str(self.index(x)) + "):" + str(x) + " of " + str(self) + ":" + str(e)
                    )

        if valtype:  # requested value type
            # fix type ambiguity for numeric
            if valtype in (int, float):
                if jsondata.isdigit():
                    jsondata = int(jsondata)
            elif valtype in (int, float):
                if jsondata.isdigit():
                    jsondata = float(jsondata)

            if not type(jsondata) is valtype:
                raise JSONPointerError("Invalid path value type:" + str(
                    type(valtype)) + " != " + str(type(jsondata)))

        else:  # in general valid value types - RFC4729,RFC7951
            if not self.isvalid_nodetype(jsondata):
                raise JSONPointerError(
                    "Invalid path nodetype:"
                    + str(type(jsondata)))

        # self.node = jsondata  # cache for reuse

        if type(jsondata) in (dict, list,):
            if cp == C_SHALLOW:  # default
                return copy.copy(jsondata)
            elif cp == C_DEEP:
                return copy.deepcopy(jsondata)

        # C_REF
        return jsondata

    def get_node(self, jsondata):
        """Returns the existing node for the pointer,
        calls transparently *JSONPointer.__call__*.

        Args:
            **jsondata**:
                A valid JSON data node.

        Returns:
            The node reference.

        Raises:
            JSONPointerError:

            pass-through

        """
        return self.__call__(jsondata)

    def get_node_exist(self, jsondata, parent=False):
        """Returns two parts, the exisitng node for valid part of
        the pointer, and the remaining part of the pointer for
        the non-existing sub-path.

        This method works similar to the 'evaluate' method, whereas it
        handles partial valid path pointers, which may also include
        a '-' in accordance to RFC6902.

        Therefore the non-ambiguous part of the pointer is resolved,
        and returned with the remaining part for a newly create.
        Thus this method is in particular foreseen to support the
        creation of new sub data structures.

        The 'evaluate' method therefore returns a list of two elements,
        the first is the node reference, the second the list of the
        remaining path pointer components. The latter may be empty in
        case of a fully valid pointer.


        Args:
            **jsondata**:
                A valid JSON data node.

            **parent**:
                Return the parent node of the pointed value.

        Returns:
            The node reference, and the remaining part.
            ret:=(node, [<remaining-path-components-list>])

        Raises:
            JSONPointerError:
            forwarded from json
        """
        if super(JSONPointer, self).__eq__([]):  # special RFC6901, whole document
            return (jsondata, None)
        if super(JSONPointer, self).__eq__(['']):  # special RFC6901, '/' empty top-tag
            return (jsondata[''], None)

        if type(jsondata) not in (dict, list, JSONData):
            # concrete info for debugging for type mismatch
            raise JSONPointerError("Invalid nodetype parameter:" +
                                       str(type(jsondata)))
        remaining = None
        try:
            if parent:
                for x in self[:-1]:
                    remaining = x
                    # want the exception, the keys within the process has to match
                    jsondata = jsondata[x]
            else:
                for x in self:
                    remaining = x
                    # want the exception, the keys within the process has to match
                    jsondata = jsondata[x]
        except Exception:
            if parent:
                remaining = self[self.index(remaining):-1]
            else:
                remaining = self[self.index(remaining):]
        else:
            remaining = None

        if type(jsondata) not in (dict, list):
            # concrete info for debugging for type mismatch
            raise JSONPointerError("Invalid path nodetype:" +
                                       str(type(jsondata)))
        self.node = jsondata  # cache for reuse
        return (jsondata, remaining,)

    def get_path_list(self):
        """Gets for the corresponding path list of the object pointer for
        in-memory access on the data of the 'json' package.

        Args:
            none

        Returns:
            The path list.

        Raises:
            none
        """
        if __debug__:
            if self.debug:
                print(repr(self))
        return list(self)

    def get_path_list_and_key(self):
        """Gets for the corresponding path list of the object pointer for in-memory access on the data of the 'json' package.

        Args:
            none

        Returns:
            The path list.

        Raises:
            none
        """
        if len(self) > 2:
            return self[:-1], self[-1]
        elif len(self) == 1:
            return [], self[-1]
        elif len(self) == 0:
            return [], None

    def get_pointer(self, jsondata=None, **kargs):
        """Gets the object pointer in compliance to RFC6901
        or relative pointer/draft-01/2018.

        The result is by default the assigned pointer itself without
        verification. Similar in case of a relative pointer the start
        offset is ignored by default and no verification is performed.

        The following options modify this behaviour:

        * superpose - superposes the *startrel* offset with the pointer
        * verify - verifies the actual existence of the nodes and/or
          intermediate nodes

        The options could be applied combined.

        Args:
            kargs:
                **returntype**:
                    Defines the return type. ::

                       returntype := (
                            RT_DEFAULT     | 'default'
                          | RT_LST         | 'list'      | list
                          | RT_JSONPOINTER | 'jpointer'
                       )

                **superpose**:
                    Is only relevant for relative paths. Superposes the offset
                    *startrel* with the pointer into the resulting final pointer.
                    By default nodes are not verified, see *verify* parameter.

                    default := True

                **verify**:
                    Verifies the "road" of the superposed pointers. ::

                       verify := (
                            V_DEFAULT | 'default'
                          | V_NONE    | 'none'    | None    # no checks at all
                          | V_FINAL   | 'final'             # checks final result only
                          | V_STEPS   | 'steps'             # checks each intermediate directory
                       )

                    default := None
        Returns:
            The new pointer in a choosen format, see *returntype*.

        Raises:
            none
        """
        returntype = rtypes2num[kargs.get('returntype')]
        verify = verify2num[kargs.get('verify')]

        superpose = kargs.get('superpose', True)

        # returned pointer
        _ptr = JSONPointer(self)

        if self.__isrel:
            if superpose:
                #    - superpose the rfc6901 and the startrel pointers

                #
                # first calculate by ignoring jsondata,
                # but checks consistency of integer-prefix
                # and start-node-pointer
                #

                # depth from pointer root to start with __startrel,
                # calc whether int-prefix larger than the length of the offset
                ix = len(self.__startrel) - self.__relupidx
                if ix < 0:
                    raise JSONPointerError(
                        "offset is shorter than integer-index startrel:%s - int-idx=%s" % (
                        len(self.__startrel), self.__relupidx)
                        )

                if ix == 0:
                    _ptr = self

                else:
                    _ptr = self.__startrel[:ix]
                    _ptr.extend(self)

                #
                # now perform optional verification
                #

                if verify & V_FINAL:
                    # check final only
                    _chk = JSONPointer(_ptr)(jsondata)

                elif verify & V_STEPS:
                    #
                    # check intermediate anchors by stepwise verification
                    #

                    # check offset pointer , and get node
                    _chk = JSONPointer(self.__startrel)(jsondata)

                    # check int-prefix ends within document, and get node
                    _chk = JSONPointer(self.__relupidx + '#')(_chk)

                    # check pointer ends within document, and get node
                    _chk = JSONPointer(self)(_chk)

        #
        # cast return type
        #
        if returntype & RT_JSONPOINTER:
            return _ptr
        elif returntype & RT_LST:
            return list(_ptr)
        else:
            raise JSONPointerError("Unknown return type: " + str(returntype))

    def get_pointer_and_key(self, jsondata=None, **kargs):
        """Get the resulting pointer and key from the processing of
        the pointer and the optional starting node *stratrel*.
        """
        ret = self.get_pointer(jsondata, **kargs)
        k = ret.pop()
        return (ret, k,)

    def get_pointer_str(self, jsondata=None, **kargs):
        """Gets the objects pointer string in compliance to RFC6901
        or relative pointer/draft-01/2018.

        The result is by default the assigned pointer itself without
        verification. Similar in case of a relative pointer the start
        offset is ignored by default and no verification is performed.

        The following options modify this behaviour:

        * superpose - superposes the *startrel* offset with the pointer
        * verify - verifies the actual existence of the nodes and/or
          intermediate nodes

        The options could be applied combined.

        Args:
            kargs:
                **forcenotation**:
                    Force the output notation for string representation to: ::

                       forcenotation := (
                            NOTATION_NATIVE           # original format with unescape
                          | NOTATION_JSON             # transform to resulting pointer
                          | NOTATION_HTTP_FRAGMENT    # return a fragment with encoding
                          | NOTATION_JSON_REL         # resulting relative pointer
                          | NOTATION_RAW              # raw input
                       )

                       default := NOTATION_NATIVE

                    **REMINDER**: Applicable for return type string only.

                **superpose**:
                    Is only relevant for relative paths. Superposes the offset
                    *startrel* with the pointer into the resulting final pointer.
                    By default nodes are not verified, see *verify* parameter.

        Returns:
            The new pointer in a choosen format, see *returntype*.

        Raises:
            none
        """
        forcenotation = kargs.get('forcenotation')
        superpose = kargs.get('superpose', False)

        #
        # notation is only relevant for string representation,
        # while the internal technical representation is almost neutral
        #
        if forcenotation == NOTATION_JSON:
            if self.__isrel:
                if self.__isrelpathrequest:
                    ret = self.__start.copy()
                else:
                    return self.__start + '#'
            else:
                if super(JSONPointer,self).__eq__([]):
                    return '""'
                ret = '/'

        elif forcenotation == NOTATION_HTTP_FRAGMENT:
            if self.__isrel:
                if self.__isrelpathrequest:
                    ret = self.__start
                else:
                    return self.__start
            else:
                return '/'

        elif forcenotation == NOTATION_JSON_REL:
            if self.__isrel:
                if self.__isrelpathrequest:
                    ret = self.__start
                else:
                    return self.__start
            else:
                return '/'

        else:  # NOTATION_NATIVE
            #
            # set the appropriate prefix:
            #   rfc6901-pointer, rfc6901-uri-fragment-pointer,
            #   relpath-draft-1
            #
            if self.__isfragment:  # rfc6901 - uri-fragment
                if not self:  # special - whole document
                    ret = '#'
                else:  # a subpath
                    ret = '#/'

            elif self.__isrel:  # relpointer
                if self.__isrelpathrequest:  # is get relpath request
                    if superpose:
                        ix = len(self.__startrel) - self.__relupidx
                        if ix < 0:
                            raise JSONPointerError(
                                "offset is shorter than integer-index startrel:%s - int-idx=%s" % (
                                len(self.__startrel), self.__relupidx)
                                )

                        if ix == 0:
                            _ptr = self

                        else:
                            _ptr = self.__startrel[:ix]
                            _ptr.extend(self)
                    else:
                        _ptr = self

                    if super(JSONPointer, self).__eq__([]):
                        if _ptr:
                            return unicode('/' + '/'.join(map(unicode, _ptr)) + '/')
                        else:
                            return unicode('""')
                    else:
                        return unicode('/' + '/'.join(map(unicode, _ptr)))

                else:  # is get-key/index - request
                    return str(self.__relupidx) + '#'

            else:  # rfc6901 - in-document-absolute pointer
                if not self:  # ==[] : special RFC6901, whole document
                    return ''
                ret = '/'

                if len(self) == 1 and self[0] == '':  # special RFC6901, '/' empty top-tag
                    return '/'


        return unicode(ret + '/'.join(map(unicode, self)))

    def get_raw(self):
        """Gets the objects raw 6901-pointer.

        Args:
            none

        Returns:
            The raw path.

        Raises:
            none
        """
        try:
            return self.__raw
        except KeyError:
            return None

    def get_relupidx(self):
        """Returns the resulting integer prefix.
        """
        try:
            return self.__relupidx
        except KeyError:
            return None

    def get_start(self):
        """Returns the resulting start pointer after the
        application of the integer prefix.
        """
        try:
            return self.__start
        except KeyError:
            return None

    def get_startrel(self):
        """Returns the raw start pointer.
        """
        try:
            return self.__startrel
        except KeyError:
            return None

    def evaluate(self, jsondata, parent=False):
        """Gets the value resulting from the current pointer.

        Args:
            **jsondata**:
                A JSON data node. ::

                   jsondata := (
                       JSONData
                       | list
                       | dict
                       )

            **parent**:
                Return the parent node of the pointed value.
                When parent is selected, the pointed child node
                is not verified.

        Returns:
            The referenced value.

        Raises:
            JSONPointerError:

            pass-through
        """
        #
        # calc starting node
        #
        if self.__isrel:
            # relative draft-1/2018

            # check whether pointed to a valid node
            if not self.__startrel.check_node_or_value(jsondata):
                raise JSONPointerError('node does not exist:"' + str(self.__startrel) + '"')

            # pointer is getrelpath request
            if self.__isrelpathrequest:
                if self.__start:  # already pre-calculated
                    _startnode = self.__start.evaluate(jsondata)
                else:
                    _startnode = jsondata

                if not self:  # special - whole rel document - integer only
                    return _startnode

            # pointer is get-key/index - request
            else:
                return self.__start.get_key()

        elif self == []:
            # special RFC6901, whole document
            return jsondata

        #
        # REMEMBER: special RFC6901, '/""' empty top-tag
        #           section 5 / pg. 5
        #
        elif len(self) == 1 and self[0] == '':
            try:
                return jsondata['']
            except KeyError as e:
                raise JSONPointerError("""Non-existent node(see RFC6901 - chap 5): '/""'""")

        else:
            # a standard rfc6901 pointer
            _startnode = jsondata

        if type(_startnode) not in (dict, list, JSONData):
            # concrete info for debugging for type mismatch
            if self.__isrel:

                raise JSONPointerError(
                    "Invalid nodetype parameter: %s"
                    "\n  pointer   = %s"
                    "\n  startrel  = %s"
                    "\n  start     = %s"
                    "\n  jsondata  = %s"
                    "\n  startnode = %s"
                    % (
                        str(type(_startnode)),
                        str(self),
                        str(self.__startrel),
                        str(self.__start),
                        str(jsondata),
                        str(_startnode),
                    ))

            else:
                raise JSONPointerError(
                    "Invalid nodetype parameter:" +
                    str(type(_startnode)))

        try:
            if parent:
                for x in self[:-1]:
                    # want the exception, the keys within the process has to match
                    try:
                        _startnode = _startnode[x]
                    except TypeError as e:
                        if x == '-':
                            _startnode = _startnode[-1]
                        else:
                            try:
                                # special python - reverse index
                                _startnode = _startnode[int(x)]
                            except ValueError:
                                # now safe to give it up
                                # raise e
                                raise JSONPointerError(repr(e))
            else:
                for x in self:
                    try:
                        # standard index 0<=x<infinite
                        _startnode = _startnode[x]

                    except TypeError as e:
                        if x == '-':
                            # special rfc6901
                            _startnode = _startnode[-1]
                        else:
                            try:
                                # special python - reverse index
                                _startnode = _startnode[int(x)]
                            except ValueError:
                                # now safe to give it up
                                # raise e
                                raise JSONPointerError(repr(e))

        except Exception as e:
            if V3K:
                if isinstance(_startnode, JSONData):
                    _startnode = _startnode.data

                if type(_startnode) is dict:
                    _jdat = _startnode.keys()
                elif type(_startnode) is list:
                    _jdat = '[0...' + str(len(_startnode) - 1) + ']'
                else:
                    _jdat = _startnode

                raise JSONPointerError(
                    "Requires existing Node(jsondata[" + str(self.index(x)) + "]):"
                    + '"' + str(self) + '":' + repr(e) + ':jsondata(keys/indexes)=' + str(_jdat)
                    #
                    # TODO: update doctool for python3 introspection before re-activation
                    #
                    ) # from None

            else:
                raise JSONPointerError(
                    "Requires existing Node(jsondata[" + str(self.index(x)) + "]):"
                    + '"' + str(self) + '":' + repr(e) + ':jsondata=' + str(_startnode)
                    )

        self.node = _startnode  # cache for reuse
        return _startnode

    def isfragment(self):
        """Checks whether a http fragment."""
        return self.__isfragment

    def isrelpathrequest(self):
        """Checks whether a path request."""
        try:
            return self.__isrelpathrequest and self.__isrel
        except KeyError:
            return False

    def isrel(self):
        """Checks whether a relative pointer."""
        return self.__isrel

    def isvalid_nodetype(self, x):
        """Checks valid node types of in-memory JSON data."""
        return type(x) in  VALID_NODE_TYPE_X or x == None

    def isvalrequest(self):
        """Checks whether a value request."""
        return not self.__isvalrequest and self.__isrel

    def iter_path(self, jsondata=None, **kargs):
        """Iterator for the elements of the path pointer itself.

        Args:
            **jsondata**:
                If provided a valid JSON data node, the
                path components are successively verified on
                the provided document.

            kargs:
                **parent**:
                    Uses the path pointer to parent node.

                **rev**:
                    Reverse the order, start with last.

                **superpose**:
                    Is only relevant for relative paths, for *rfc6901* defined
                    paths the parameter is ignored. When *True* superposes
                    the offset *startrel* with the pointer into the resulting
                    final pointer. By default nodes are not verified,
                    see *verify* parameter. ::

                       superpose := (
                            True   # iterates resulting paths from *startrel*
                          | False  # iterates the path only
                       )


                    default := True

        Returns:
            Yields the iterator for the current path pointer
            components.

        Raises:
            JSONPointerError:
            forwarded from json
        """
        parent=kargs.get('parent', False)
        rev=kargs.get('rev', False)
        superpose=kargs.get('superpose', True)

        _ptr = self.get_pointer(jsondata, superpose=superpose)

        if self == []:  # special RFC6901, whole document
            yield ''
        elif self == ['']:  # special RFC6901, '/' empty top-tag
            yield '/'
        else:
            if rev:  # reverse
                if parent:  # for parent
                    ptrpath = _ptr[:-1:-1]
                else:  # full path
                    ptrpath = _ptr[::-1]
            else:
                if parent:  # for parent
                    ptrpath = _ptr[:-1]
                else:  # full path
                    ptrpath = _ptr

            try:
                x = ptrpath[0]
                for x in ptrpath:
                    if jsondata:
                        # want the exception, the keys within the process has to match
                        jsondata = jsondata[x]
                    yield x

            except Exception as e:
                if V3K:
                    raise JSONPointerError(
                        "Node(" + str(ptrpath.index(x)) +"):" + str(x) + " of " +
                        str(self) + ":" + repr(e)
                        #
                        # TODO: update doctool for python3 introspection
                        #
                        ) # from None
                else:
                    raise JSONPointerError(
                        "Node(" + str(ptrpath.index(x)) +"):" + str(x) + " of " +
                        str(self) + ":" + repr(e)
                        )

            self.node = jsondata  # cache for reuse

    def iter_path_nodes(self, jsondata, parent=False, rev=False):
        """Iterator for the elements the path pointer points to.

        Args:
            **jsondata**:
                A valid JSON data node.

            **parent**:
                Uses the path pointer to parent node.

            **rev**:
                Reverse the order, start with last.

        Returns:
            Yields the iterator of the current node reference.

        Raises:
            JSONPointerError:
            forwarded from json
        """
        if self == []:  # special RFC6901, whole document
            yield jsondata
        elif self == ['']:  # special RFC6901, '/' empty top-tag
            yield jsondata['']
        else:
            if rev:  # reverse
                if parent:  # for parent
                    ptrpath = self[:-1:-1]
                else:  # full path
                    ptrpath = self[::-1]
            else:
                if parent:  # for parent
                    ptrpath = self[:-1]
                else:  # full path
                    ptrpath = self

            try:
                x = ptrpath[0]
                for x in ptrpath:
                    # want the exception, the keys within the process has to match
                    jsondata = jsondata[x]
                    yield jsondata
            except Exception as e:
                if V3K:
                    raise JSONPointerError(
                        "Node(" + str(ptrpath.index(x)) +"):" + str(x) + " of " +
                        str(self) + ":" + repr(e)
                        #
                        # TODO: update doctool for python3 introspection
                        #
                        ) # from None
                else:
                    raise JSONPointerError(
                        "Node(" + str(ptrpath.index(x)) +"):" + str(x) + " of " +
                        str(self) + ":" + repr(e)
                        )

            self.node = jsondata  # cache for reuse

    def iter_path_subpaths(self, jsondata=None, parent=False, rev=False):
        """Successive iterator for the resulting sub-paths the
        path pointer itself.

        Args:
            **jsondata**:
                If provided a valid JSON data node, the
                path components are successively verified on
                the provided document.

            **parent**:
                Uses the path pointer to parent node.

            **rev**:
                Reverse the order, start with last.

        Returns:
            Yields the iterator for the copy of the current
            slice of the path pointer.

        Raises:
            JSONPointerError:
            forwarded from json
        """
        if self == []:  # special RFC6901, whole document
            yield ''
        elif self == ['']:  # special RFC6901, '/' empty top-tag
            yield '/'
        else:
            curpath = []
            if rev:  # reverse
                if parent:  # for parent
                    ptrpath = self[:-1:-1]
                else:  # full path
                    ptrpath = self[::-1]
            else:
                if parent:  # for parent
                    ptrpath = self[:-1]
                else:  # full path
                    ptrpath = self

            try:
                x = ptrpath[0]
                for x in ptrpath:
                    if jsondata:
                        # want the exception, the keys within the process has to match
                        jsondata = jsondata[x]
                    curpath.append(x)
                    yield curpath[:]
            except Exception as e:
                if V3K:
                    raise JSONPointerError(
                        "Node(" + str(ptrpath.index(x)) +"):" + str(x) + " of " +
                        str(self) + ":" + repr(e)
                        #
                        # TODO: update doctool for python3 introspection
                        #
                        ) # from None
                else:
                    raise JSONPointerError(
                        "Node(" + str(ptrpath.index(x)) +"):" + str(x) + " of " +
                        str(self) + ":" + repr(e)
                        )

    def iter_path_subpathdata(self, jsondata=None, parent=False, rev=False):
        """Successive iterator for the resulting sub-paths and the
        corresponding nodes.

        Args:
            **jsondata**:
                If provided a valid JSON data node, the
                path components are successively verified on
                the provided document.

            **parent**:
                Uses the path pointer to parent node.

            **rev**:
                Reverse the order, start with last.

        Returns:
            Yields the iterator for the tuple of the current
            slice of the path pointer and the reference of the
            corresponding node. ::

               (<path-item>, <sub-path>, <node>)

               path-item: copy of the item
               sub-path:  copy of the current subpath
               node:      reference to the corresponding node

        Raises:
            JSONPointerError:
            forwarded from json
        """
        if self == []:  # special RFC6901, whole document
            yield ''
        elif self == ['']:  # special RFC6901, '/' empty top-tag
            yield '/'
        else:
            curpath = []
            if rev:  # reverse
                if parent:  # for parent
                    ptrpath = self[:-1:-1]
                else:  # full path
                    ptrpath = self[::-1]
            else:
                if parent:  # for parent
                    ptrpath = self[:-1]
                else:  # full path
                    ptrpath = self

            try:
                x = ptrpath[0]
                for x in ptrpath:
                    if jsondata:
                        # want the exception, the keys within the process has to match
                        jsondata = jsondata[x]
                    curpath.append(x)
                    yield (x, curpath[:], jsondata)
            except Exception as e:
                if V3K:
                    raise JSONPointerError(
                        "Node(" + str(ptrpath.index(x)) +"):" + str(x) + " of " +
                        str(self) + ":" + repr(e)
                        #
                        # TODO: update doctool for python3 introspection
                        #
                        ) # from None
                else:
                    raise JSONPointerError(
                        "Node(" + str(ptrpath.index(x)) +"):" + str(x) + " of " +
                        str(self) + ":" + repr(e)
                        )

            self.node = jsondata  # cache for reuse

from jsondata.jsondata import JSONData
VALID_NODE_TYPE_X = (
    dict,
    list,
    str,
    unicode,
    int,
    float,
    bool,
    None,
    JSONData,)
"""Valid types of in-memory JSON node types for processing."""
