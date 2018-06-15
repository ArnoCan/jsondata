# -*- coding:utf-8   -*-
"""The JSONPatch module provides for the alteration of JSON data compliant to RFC6902.
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import sys
import copy

# pylint: disable-msg=F0401
if sys.modules.get('json'):
    import json as myjson  # @UnusedImport
elif sys.modules.get('ujson'):
    import ujson as myjson  # @UnusedImport @Reimport @UnresolvedImport
else:
    import json as myjson  # @Reimport
# pylint: enable-msg=F0401

# for now the only one supported
from jsondata.jsonpointer import JSONPointer
from jsondata.jsondataserializer import JSONDataSerializer, MS_OFF
from jsondata.jsondata import JSONData
from jsondata import V3K, JSONDataPatchError, JSONDataPatchItemError, \
    C_SHALLOW, C_DEEP, C_REF, \
    SD_INPUT, SD_OUTPUT


__author__ = 'Arno-Can Uestuensoez'
__maintainer__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez" \
                " @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.21'
__uuid__ = '63b597d6-4ada-4880-9f99-f5e0961351fb'

if V3K:
    unicode = str

# Sets display for inetractive JSON/JSONschema design.
_interactive = False

#
# Operations in accordance to RFC6902
RFC6902_ADD = 1
RFC6902_COPY = 2
RFC6902_MOVE = 3
RFC6902_REMOVE = 4
RFC6902_REPLACE = 5
RFC6902_TEST = 6

#
# Mapping for reverse transformation
op2str = {
    RFC6902_ADD: "add",
    RFC6902_COPY: "copy",
    RFC6902_MOVE: "move",
    RFC6902_REMOVE: "remove",
    RFC6902_REPLACE: "replace",
    RFC6902_TEST: "test"
}

#
# Mapping for reverse transformation
str2op = {
    "add": RFC6902_ADD,
    "copy": RFC6902_COPY,
    "move": RFC6902_MOVE,
    "remove": RFC6902_REMOVE,
    "replace": RFC6902_REPLACE,
    "test": RFC6902_TEST
}


def getOp(x):
    """Converts input into corresponding enumeration.
    """
    if type(x) in (
            int,
            float, ):
        return int(x)
    elif type(x) is (
            str,
            unicode, ) and x.isdigit():
        return int(x)
    return str2op.get(x, None)


class JSONPatchItem(object):
    """Record entry for list of patch tasks.

    Attributes:
        **op**:
            operations: ::

               add, copy, move, remove, replace, test

        **target**:
            JSONPointer for the modification target, see RFC6902.

        **value**:
            Value, either a branch, or a leaf of the JSON data structure.

        **src**:
            JSONPointer for the modification source, see RFC6902.

    """

    def __init__(self, op, target, param=None, **kargs):
        """Create an entry for the patch list.

        Args:
            **op**:
                Operation: ::

                   add, copy, move, remove, replace, test

            **target**:
                Target node. ::

                   target := (
                       <rfc6901-string>
                       | JSONPointer
                       | <path-items-list>
                       )

            **param**:
                Specific parameter for the operation.

                +-------+--------------------+
                | type  | operation          |
                +=======+====================+
                | value | add, replace, test |
                +-------+--------------------+
                | src   | copy, move         |
                +-------+--------------------+
                | param | None for 'remove'  |
                +-------+--------------------+

            kargs:
                **replace**:
                    Replace masked characters in *target* specification. ::

                       replace := (
                            True    # replaces rfc6901 escape sequences: ~0 and ~1
                          | False   # omit unescaping
                       )

                    .. note::
                    
                       Match operations are proceeded literally, thus the
                       escaped characters should be consistent,
                       see rfc6901, Section 3.

                    default := False

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.
            Success is the complete addition only, thus one failure returns
            False.

        Raises:
            JSONDataPatchItemError

        """
        self.replace = kargs.get('replace', False) 

        self.value = None
        self.src = None

        self.op = getOp(op)
        self.target = JSONPointer(target, replace=self.replace)

        if self.op in (RFC6902_ADD, RFC6902_REPLACE, RFC6902_TEST):
            self.value = param

        elif self.op is RFC6902_REMOVE:
            pass

        elif self.op in (RFC6902_COPY, RFC6902_MOVE):
            self.src = param

        else:
            raise JSONDataPatchItemError("Unknown operation.")

    def __add__(self, x=None):
        if x == None:
            raise JSONDataPatchError("Missing patch entry/patch")
        if isinstance(x, JSONPatchItem):
            ret = JSONPatch()
            ret.patch.append(self)
            ret.patch.append(x)
            return ret
        elif isinstance(x, JSONPatch):
            ret = JSONPatch(x.patch)
            ret.patch.insert(0, self)
            return ret
        else:
            raise JSONDataPatchError("Unknown input" + type(x))

    def __call__(self, jdata):
        """Evaluates the related task for the provided data.

        Args:
            **jdata**:
                JSON data the task has to be 
                applied on.

        Returns:
            Returns a tuple of: ::

               (n,lerr): 

               n:    number of present active entries
               lerr: list of failed entries

        Raises:
            JSONDataPatchError:
        """
        return self.apply(jdata)

    def __eq__(self, x=None):
        """Compares this pointer with x.

        Args:
            **x**:
                A valid Pointer.

        Returns:
            *True* or *False*.

        Raises:
            JSONPointerError
        """
        if x == None:
            return False

        ret = True

        if type(x) == dict:
            ret &= self.target == x['path']
        else:
            ret &= self.target == x['target']

        if self.op == RFC6902_ADD:
            ret &= x['op'] in ('add', RFC6902_ADD)
            ret &= self.value == x['value']
        elif self.op == RFC6902_REMOVE:
            ret &= x['op'] in ('remove', RFC6902_REMOVE)
        elif self.op == RFC6902_REPLACE:
            ret &= x['op'] in ('replace', RFC6902_REPLACE)
            ret &= self.value == x['value']
        elif self.op == RFC6902_MOVE:
            ret &= x['op'] in ('move', RFC6902_MOVE)
            ret &= self.src == x['from']
        elif self.op == RFC6902_COPY:
            ret &= x['op'] in ('copy', RFC6902_COPY)
            ret &= self.src == x['from']
        elif self.op == RFC6902_TEST:
            ret &= x['op'] in ('test', RFC6902_TEST)
            ret &= self.value == x['value']

        return ret

    def __getitem__(self, key):
        """Support of various mappings.

            #. self[key]

            #. self[i:j:k]

            #. x in self

            #. for x in self

        """
        if key in (
                'path',
                'target', ):
            return self.target
        elif key in ('op', ):
            return self.op
        elif key in (
                'value',
                'param', ):
            return self.value
        elif key in (
                'from',
                'src', ):
            return self.src

    def __ne__(self, x):
        """Compares this pointer with x.

        Args:
            **x**: A valid Pointer.

        Returns:
            *True* or *False*.

        Raises:
            JSONPointerError
        """
        return not self.__eq__(x)

    def __radd__(self, x=None):
        if x == None:
            raise JSONDataPatchError("Missing patch entry/patch")
        if isinstance(x, JSONPatchItem):
            ret = JSONPatch()
            ret.patch.append(x)
            ret.patch.append(self)
            return ret
        elif isinstance(x, JSONPatch):
            ret = JSONPatch()
            ret.patch.extend(x.patch)
            ret.patch.append(self)
            return ret
        else:
            raise JSONDataPatchError("Unknown input" + type(x))

    def __repr__(self):
        """Prints the patch string in accordance to RFC6901.
        """
        ret = '{"op": "' + unicode(op2str[self.op]) + \
            '", "path": "' + unicode(self.target) + '"'
        if self.op in (RFC6902_ADD, RFC6902_REPLACE, RFC6902_TEST):
            if type(self.value) in (int, float):
                ret += ', "value": ' + unicode(self.value)
            elif type(self.value) in (dict, list):
                ret += ', "value": ' + repr(self.value)
            else:
                ret += ', "value": "' + unicode(self.value) + '"'

        elif self.op is RFC6902_REMOVE:
            pass

        elif self.op in (RFC6902_COPY, RFC6902_MOVE):
            ret += ', "from": "' + unicode(self.src) + '"'
        ret += "}"
        return ret

    def __str__(self):
        """Prints the patch string in accordance to RFC6901.
        """
        ret = '{"op": "' + op2str[self.op] + \
            '", "target": "' + str(self.target)
        if self.op in (RFC6902_ADD, RFC6902_REPLACE, RFC6902_TEST):
            if type(self.value) in (int, float):
                ret += '", "value": ' + str(self.value) + ' }'
            else:
                ret += '", "value": "' + str(self.value) + '" }'

        elif self.op is RFC6902_REMOVE:
            ret += '" }'

        elif self.op in (RFC6902_COPY, RFC6902_MOVE):
            ret += '", "src": "' + str(self.src) + '" }'
        return ret

    def apply(self, jsondata, **kargs):
        """Applies the present patch list on the provided JSON document.

        Args:
            **jsondata**:
                Document to be patched.

            kargs:
                **replace**:
                    Replace masked characters in *target* specification. ::

                       replace := (
                            True    # replaces rfc6901 escape sequences: ~0 and ~1
                          | False   # omit unescaping
                       )

                    .. note::
                    
                       Match operations are proceeded literally, thus the
                       escaped characters should be consistent,
                       see rfc6901, Section 3.

                       If already decoded e.g. by the constructor, than should be
                       *FALSE*, is not idempotent.

                    default := False
            
        Returns:
            When successful returns 'True', else raises an exception.
            Or returns a tuple: ::

               (n,lerr): 

               n:    number of present active entries
               lerr: list of failed entries

        Raises:
            JSONDataPatchError:
        """
        replace = kargs.get('replace', self.replace) 

        if self.op is RFC6902_ADD:
            return jsondata.branch_add(
                self.value, self.target)

        if isinstance(jsondata, JSONDataSerializer):
            jsondata = jsondata.data

        if self.op is RFC6902_REPLACE:
            n, b = self.target.get_node_and_key(jsondata)
            n[b] = self.value

        elif self.op is RFC6902_TEST:
            n, b = JSONPointer(self.target, replace=replace).get_node_and_key(jsondata)
#             if type(self.value) is str:
#                 self.value = unicode(self.value)
#             if type(n) is list:
#                 return n[b] == self.value
#             return n[unicode(b)] == self.value
            if isinstance(n, list):
                return n[int(b)] == self.value
            elif isinstance(n, dict):
                return n[unicode(b)] == self.value

        elif self.op is RFC6902_COPY:
            val = JSONPointer(self.src, replace=replace).get_node_value(jsondata)
            tn, tc = self.target.get_node_and_key(jsondata)
            tn[tc] = val

        elif self.op is RFC6902_MOVE:
            val = JSONPointer(self.src, replace=replace).get_node_value(jsondata)
            sn, sc = JSONPointer(self.src, replace=replace).get_node_and_key(jsondata)
            sn.pop(sc)
            tn, tc = self.target.get_node_and_key(jsondata)
            if type(tn) is list:
                if len(tn) <= tc:
                    tn.append(val)
                else:
                    tn[tc] = val
            else:
                tn[tc] = val

        elif self.op is RFC6902_REMOVE:
            n, b = self.target.get_node_and_key(jsondata)
            n.pop(b)

        return True

    def repr_export(self):
        """Prints the patch string for export in accordance to RFC6901.
        """
        ret = '{"op": "' + str(op2str[self.op]) + \
            '", "path": "' + str(self.target) + '"'
        if self.op in (RFC6902_ADD, RFC6902_REPLACE, RFC6902_TEST):
            if type(self.value) in (int, float):
                ret += ', "value": ' + str(self.value)
            elif type(self.value) in (dict, list):
                ret += ', "value": ' + str(self.value)
            elif type(self.value) is None:
                ret += ', "value": null'
            elif type(self.value) is False:
                ret += ', "value": false'
            elif type(self.value) is True:
                ret += ', "value": true'
            else:
                ret += ', "value": "' + str(self.value) + '"'

        elif self.op is RFC6902_REMOVE:
            pass

        elif self.op in (RFC6902_COPY, RFC6902_MOVE):
            ret += ', "from": "' + str(self.src) + '"'
        ret += '}'
        return ret

    def str_export(self):
        """Pretty prints the patch string for export in accordance to RFC6901.
        """
        ret = '{"op": "' + str(op2str[self.op]) + \
            '", "path": "' + str(self.target) + '"'
        if self.op in (RFC6902_ADD, RFC6902_REPLACE, RFC6902_TEST):
            if type(self.value) in (int, float):
                ret += ', "value": ' + str(self.value)
            elif type(self.value) in (dict, list):
                ret += ', "value": ' + str(self.value)
            elif type(self.value) is None:
                ret += ', "value": null'
            elif type(self.value) is False:
                ret += ', "value": false'
            elif type(self.value) is True:
                ret += ', "value": true'
            else:
                ret += ', "value": "' + str(self.value) + '"'

        elif self.op is RFC6902_REMOVE:
            pass

        elif self.op in (RFC6902_COPY, RFC6902_MOVE):
            ret += ', "from": "' + str(self.src) + '"'
        ret += '}'
        return ret

class JSONPatchItemRaw(JSONPatchItem):
    """Adds native patch strings or an unsorted dict for RFC6902.
    
    Calls parent *JSONPatchItem*.

    """

    def __init__(self, patchstring, **kargs):
        """Parse a raw patch string in accordance to RFC6902.
        """
        self.replace = kargs.get('replace', False) 

        if type(patchstring) in (
                str,
                unicode, ):
            ps = myjson.loads(patchstring)
            sx = myjson.dumps(ps)
            if len(sx.replace(" ", "")) != len(patchstring.replace(" ", "")):
                raise JSONDataPatchItemError(
                    "Repetition is not compliant to RFC6902:" +
                    str(patchstring))
        elif type(patchstring) is dict:
            ps = patchstring
        else:
            raise JSONDataPatchItemError("Type not supported:" +
                                         str(patchstring))

        try:
            target = ps['path']
            op = getOp(ps['op'])

            if op in (RFC6902_ADD, RFC6902_REPLACE, RFC6902_TEST):
                param = ps['value']

            elif op is RFC6902_REMOVE:
                param = None

            elif op in (RFC6902_COPY, RFC6902_MOVE):
                param = ps['from']
        except Exception as e:
            raise JSONDataPatchItemError(e)

        super(JSONPatchItemRaw, self).__init__(op, target, param, **kargs)


class JSONPatchFilter(object):
    """Filtering capabilities on the entries of patch lists.
    
    .. warning::
    
       Not yet implemented.

    """

    def __init__(self, **kargs):
        """
        Args:
            kargs:
                Filter parameters:

                **common**:

                    contain=(True|False): Contain, else equal.

                    type=<node-type>: Node is of type.

                **paths**:

                    branch=<branch>: 

                    deep=(): Determines the depth of comparison.

                    prefix=<prefix>: Any node of prefix. If prefix is
                        absolute: the only and one, else None.
                        relative: any node prefixed by the path fragment.

                **values**:
                    val=<node-value>: Node ha the value.


        Returns:
            True or False

        Raises:
            JSONPointerError:
        """
        for k, v in kargs:
            if k == 'prefix':
                self.prefix = v
            elif k == 'branch':
                self.branch = v

    def __eq__(self, x):

        pass

    def __ne__(self, x):

        pass


class JSONPatch(object):
    """ Representation of a JSONPatch task list for RFC6902.

    Contains the defined methods from standards:

    * add
    * remove
    * replace
    * move
    * copy
    * test

    Attributes:
        **patch**:
            List of patch items.

    """

    def __init__(self, p=None, **kargs):
        """List of patch tasks.

        Args:
            **p**:
                Patch list. ::

                   p := (
                        JSONPatch
                      | <list-of-patch-items>
                   )

            kargs:
                **replace**:
                    Replace masked characters in *target* specification. ::

                       replace := (
                            True    # replaces rfc6901 escape sequences: ~0 and ~1
                          | False   # omit unescaping
                       )

                    .. note::
                    
                       Match operations are proceeded literally, thus the
                       escaped characters should be consistent,
                       see rfc6901, Section 3.

                    default := False

        Returns:
            self.

        Raises:
            pass-through
        """
        assert isinstance(p, list) or p == None

        self.replace = kargs.get('replace', False) 

        if p:
            self.patch = p
        else:
            self.patch = []

        self.deep = False
        """Defines copy operations, True:=deep, False:=swallow"""

    def __add__(self, x=None):
        """Creates and adds patch job to the task queue.
        
        Args:
            **x**:
                Extension of pathc job, eithe a *JSONPatch*,
                or a *JSONPatchItem*.

        Returns:
            Returns a patch job, or raises Exception. 

        Raises:
            JSONDataPatchError

        """
        if x == None:
            raise JSONDataPatchError("Missing patch entry/patch")
        if isinstance(x, JSONPatchItem):
            ret = JSONPatch(self.patch)
            ret.patch.append(x)
            return ret
        elif isinstance(x, JSONPatch):
            ret = JSONPatch(self.patch)
            ret.patch.extend(x.patch)
            return ret
        else:
            raise JSONDataPatchError("Unknown input" + type(x))

    def __call__(self, jdata, x=None):
        """Evaluates the related task for the provided index.

        Args:
            **x**: 
                Task index.

            **jdata**: 
                JSON data the task has to be 
                applied on.

        Returns:
            Returns a tuple of: ::

               (n, lerr): 

               n:    number of present active entries
               lerr: list of failed entries

        Raises:
            JSONDataPatchError:
        """
        if x  is None:
            return self.apply(jdata)
        if self.patch[x](jdata):
            return 1, []
        return 1, [0]

    def __eq__(self, x):
        """Compares this pointer with x.

        Args:
            **x**:
                A valid Pointer.

        Returns:
            *True* or *False*

        Raises:
            JSONPointerError
        """
        if x == None:
            return False

        match = len(self.patch)
        if match != len(x):
            return False

        if isinstance(x, JSONPatch):
            return self.patch == x.patch
        elif isinstance(x, list):
            ret = True
            for i in range(match):
                for k in x[i].keys():
                    if k == 'op':
                        ret &= str(x[i][k]) == op2str[self.patch[i][k]] 
                    else:
                        ret &= str(x[i][k]) == str(self.patch[i][k]) 
            return ret
        else:
            raise JSONDataPatchError("Type requires JSONPatch or list, got" + str(type(x)))

    def __getitem__(self, key):
        """Support of slices, for 'iterator' refer to self.__iter__.

            #. self[key]

            #. self[i:j:k]

            #. x in self

            #. for x in self

        """
        return self.patch[key]

    def __iadd__(self, x=None):
        """Adds patch jobs to the task queue in place.
        """
        if x == None:
            raise JSONDataPatchError("Missing patch entry/patch")
        if isinstance(x, JSONPatchItem):
            self.patch.append(x)
        elif isinstance(x, JSONPatch):
            self.patch.extend(x.patch)
        else:
            raise JSONDataPatchError("Unknown input" + type(x))
        return self

    def __isub__(self, x):
        """Removes the patch job from the task queue in place. 

        Removes one of the following type(x) variants:

            *int*:
                The patch job with given index.

            *JSONPatchItem*:
                The first matching entry from 
                the task queue. 

        Args:
            **x**:
                Item to be removed. ::
    
                   x := (
                        int
                      | JSONPatchItem
                   ) 

        Returns:
            Returns resulting list without x.

        Raises:
            JSONDataPatchError:
        """
        if type(x) is int:
            self.patch.pop(x)
        else:
            self.patch.remove(x)
        return self

    def __iter__(self):
        """Provides an iterator foreseen for large amounts of in-memory patches.
        """
        return iter(self.patch)

    def __len__(self):
        """The number of outstanding patches.
        """
        return len(self.patch)

    def __ne__(self, x):
        """Compares this pointer with x.

        Args:
            **x**:
                A valid Pointer.

        Returns:
            *True* or *False*

        Raises:
            JSONPointerError
        """
        return not self.__eq__(x)

    def __radd__(self, x=None):
        """Adds a copy of xto the task queue.
        """
        if x == None:
            raise JSONDataPatchError("Missing patch entry/patch")
        if isinstance(x, JSONPatchItem):
            ret = JSONPatch(x)
            ret.patch.append(self.patch)
            return ret
        elif isinstance(x, JSONPatch):
            ret = JSONPatch(x)
            ret.patch.extend(self.patch)
            return ret
        else:
            raise JSONDataPatchError("Unknown input" + type(x))

    def __repr__(self):
        """Prints the representation format of a JSON patch list.
        """
        ret = "["
        if self.patch:
            if len(self.patch) > 1:
                for p in self.patch[:-1]:
                    ret += repr(p) + ", "
            ret += repr(self.patch[-1])
        ret += "]"
        return unicode(ret)

    def __str__(self):
        """Prints the display format.
        """
        ret = "[\n"
        if self.patch:
            if len(self.patch) > 1:
                for p in self.patch[:-1]:
                    ret += "  " + repr(p) + ",\n"
            ret += "  " + repr(self.patch[-1]) + "\n"
        ret += "]"
        return str(ret)

    def __sub__(self, x):
        """Removes the patch job from the task queue. 

        Removes one of the following type(x) variants:

            *int*:
                The patch job with given index.

            *JSONPatchItem*:
                The first matching entry from 
                the task queue. 

        Args:
            **x**:
                Item to be removed. ::

                   x := (
                        int
                      | JSONPatchItem
                   ) 

        Returns:
            Returns resulting list without x.

        Raises:
            JSONDataPatchError:
        """
        ret = JSONPatch()
        if self.deep:
            ret.patch = self.patch[:]
        else:
            ret.patch = self.patch

        if type(x) is int:
            ret.patch.pop(x)
        else:
            ret.patch.remove(x)
        return ret

    def apply(self, jsondata, **kargs):
        """Applies the JSONPatch task.

        Args:
            **jsondata**:
                JSON data the joblist has to be applied on.

        Returns:
            Returns a tuple of: ::

               (n, lerr): 

               n:    number of present active entries
               lerr: list of failed entries

        Raises:
            JSONDataPatchError:
        """
        status = []
        for p in self.patch:
            if not p.apply(jsondata, **kargs):
                # should not be called frequently
                status.append(self.patch.index(p))
        return len(self.patch), status

    def getpatchitem(self, x=None):
        """Gets the reference to a single patch item.
        
        Args:
            **x**:
                Requested item. ::

                   x := (
                        int
                      | JSONPatchItem
                   ) 

                   int:           index of patch item
                   JSONPatchItem: the reference to the patch item
            
        Returns:
            The selected patch item.

        Raises:
            None
        """
        if x == None:
            return
        if type(x) is int:
            return self.patch[x]            
        return self.patch[self.patch.index(x)]

    def getpatchitems(self, *args, **kargs):
        """Gets a list of references of patch items.
        
        Args:
            args:
                Requested items. ::

                   *args := (
                      <item>
                      | <item-list>
                      | None
                   )
                   item-list := <item>[, <item-list>]
                   item := (
                        int
                      | JSONPatchItem
                   )
                   None := "all items of the current patch list"

                   int:           index of patch item
                   JSONPatchItem: the reference to the patch item
            
            kargs:
                **idxlist**:
                    Print with index: ::

                       idxlist := (
                            True     # format: [{<index>: <JSONPatchItem>}]
                          | False    # format: [<JSONPatchItem>]
                       )

                **copydata**:
                    Creates a copy of each resulting item. ::

                       copydata := (C_DEEP | C_SHALLOW | C_REF)

                    default := C_REF  # no copy
                
        Returns:
            A list of the selected patch items.

        Raises:
            None
        """
        ret = []
        _copy = kargs.get('copydata', C_REF)

        if args and args[0] == None:
            args = self.patch

        for x in args:
            if type(x) is int:
                _c = self.patch[x]
            else:
                x = self.patch.index(x)
                _c = self.patch[x]

            if _copy == C_SHALLOW:
                _c = copy.copy(_c)
            elif _copy == C_DEEP:
                _c = copy.deepcopy(_c)

            if kargs.get('idxlist'):
                ret.append({x: _c})
            else:
                ret.append(_c)

        return ret

    def gettree(self, *args, **kargs):
        """Gets the resulting logical JSON data structure
        constructed from the patch items of the current set.
        
        Args:
            args:
                Requested items. ::

                   *args := (
                      <item>
                      | <item-list>
                      | None
                   )
                   item-list := <item>[, <item-list>]
                   item := (
                        int
                      | JSONPatchItem
                   )
                   None := "all items of the current patch list"

                   int:           index of patch item
                   JSONPatchItem: the reference to the patch item
            
            kargs:
                **data**:
                    An optional JSON data structure, when provided
                    the actual data as selected by the patch list
                    is returned. Else the paths only.

                    default := None

                **scope**:
                    Defines the source scope of the data structure. ::

                       scope := (
                            "in"   # input data, e.g. source for "copy"
                          | "out"  # output data, e.g. target for "copy
                       )

                    default := "out"

        Returns:
            The combined list of the selected patch items contained
            in an object JSONData.

        Raises:
            None
        """
        _data = kargs.get('data', None)
        _scope = kargs.get('scope', 'out')
        if _scope == 'in':
            _scope = True
        else:
            _scope = False

        _pl = self.getpatchitems(*args)

        ret = JSONData('')
        
        for x in _pl:
            if _scope == SD_INPUT:
                if x['op'] in (RFC6902_ADD,):
                    ret.branch_add('add', x['path'])  
                elif x['op'] in (RFC6902_COPY,):
                    ret.branch_add('copy', x['from'])  
                elif x['op'] in (RFC6902_MOVE,):
                    ret.branch_add('move', x['from'])  
                elif x['op'] in (RFC6902_REMOVE,):
                    ret.branch_add('remove', x['path'])  
                elif x['op'] in (RFC6902_REPLACE,):
                    ret.branch_add('replace', x['path'])  
                elif x['op'] in (RFC6902_TEST,):
                    ret.branch_add('test', x['path'])  

            elif _scope == SD_OUTPUT:
                if x['op'] in (RFC6902_ADD,):
                    ret.branch_add('add', x['path'])  
                elif x['op'] in (RFC6902_COPY,):
                    ret.branch_add('copy', x['path'])  
                elif x['op'] in (RFC6902_MOVE,):
                    ret.branch_add('move', x['path'])  
                elif x['op'] in (RFC6902_REMOVE,):
                    ret.branch_add('remove', x['path'])  
                elif x['op'] in (RFC6902_REPLACE,):
                    ret.branch_add('replace', x['path'])  
                elif x['op'] in (RFC6902_TEST,):
                    ret.branch_add('test', x['path'])  

            else:  # both
                if x['op'] in (RFC6902_ADD,):
                    ret.branch_add('add', x['path'])  
                elif x['op'] in (RFC6902_COPY,):
                    ret.branch_add('copy', x['from'])  
                    ret.branch_add('copy', x['path'])  
                elif x['op'] in (RFC6902_MOVE,):
                    ret.branch_add('move', x['from'])  
                    ret.branch_add('move', x['path'])  
                elif x['op'] in (RFC6902_REMOVE,):
                    ret.branch_add('remove', x['path'])  
                elif x['op'] in (RFC6902_REPLACE,):
                    ret.branch_add('replace', x['path'])  
                elif x['op'] in (RFC6902_TEST,):
                    ret.branch_add('test', x['path'])  

        return ret

    def patch_export(self, patchfile, schema=None, **kargs):
        """Exports the current task list.

        Args:
            **patchfile**:
                JSON patch for export.

            **schema**:
                JSON-Schema for validation of the patch list.

            kargs:
                **validator**: [default, draft3, off, ]
                    Sets schema validator for the data file.
                    The values are: ::

                       default = validate
                       draft3  = Draft3Validator
                       off     = None

                    default:= validate

                **pretty**:
                    If True exports as tree format, 
                    else all as one line.

        Returns:
            When successful returns 'True', else raises an exception.

        Raises:
            JSONDataPatchError:

        """
        pretty = kargs.get('pretty', False)

        if not pretty:
            try:
                with open(patchfile, 'w') as fp:
                    fp.writelines(self.repr_export())
            except Exception as e:
                raise JSONDataPatchError("open-" + str(e), "data.dump",
                                         str(patchfile))

        else:
            try:
                with open(patchfile, 'w') as fp:
                    fp.writelines(str(self.str_export()))
            except Exception as e:
                raise JSONDataPatchError("open-" + str(e), "data.dump",
                                         str(patchfile))

        return True

    def patch_import(self, patchfile, schemafile=None, **kargs):
        """Imports a task list.

        Args:
            **patchfile**:
                JSON patch filename containing the list of patch operations.

            **schemafile**:
                JSON-Schema filename for validation of the patch list.

            kargs:
                **replace**:
                    Replace masked characters in *target* specification. ::

                       replace := (
                            True    # replaces rfc6901 escape sequences: ~0 and ~1
                          | False   # omit unescaping
                       )

                    .. note::
                    
                       Match operations are proceeded literally, thus the
                       escaped characters should be consistent,
                       see rfc6901, Section 3.

                    default := False

                **validator**:
                    Sets schema validator for the data file.
                    Curren release relies on *jsonschema*, which
                    supports at the time of writing draft-03 and
                    draft-04.

                    The values are: ::

                        validator := (
                              MS_DRAFT3           | 'draft3'
                            | MS_DRAFT4           | 'draft4'
                            | MS_ON               | 'on'
                            | MS_OFF              | 'off'
                            | MODE_SCHEMA_DEFAULT | 'default'
                        )

                    default:= MS_OFF

        Returns:
            When successful returns 'True', else raises an exception.

        Raises:
            JSONDataPatchError:

        """
        replace = kargs.get('replace', self.replace) 
        validator = kargs.get('validator', MS_OFF)

        patchdata = JSONDataSerializer(
            [],
            datafile=patchfile,
            schemafile=schemafile,
            validator=MS_OFF,
            )

        for pi in patchdata.data:
            self += JSONPatchItemRaw(pi, replace=replace)
        return True

    def repr_export(self):
        """Prints the export representation format of a JSON patch list.
        """
        ret = "["
        if self.patch:
            if len(self.patch) > 1:
                for p in self.patch[:-1]:
                    ret += p.repr_export() + ", "
            ret += self.patch[-1].repr_export()
        ret += "]"
        return ret

    def str_export(self):
        """Pretty prints the export representation format of a JSON patch list.
        """
        ret = "[\n"
        if self.patch:
            if len(self.patch) > 1:
                for p in self.patch[:-1]:
                    ret += "  " + p.str_export() + ",\n"
            ret += "  " + self.patch[-1].str_export() + "\n"
        ret += "]"
        return str(ret)
